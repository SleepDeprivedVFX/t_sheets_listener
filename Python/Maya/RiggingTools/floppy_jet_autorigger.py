"""
Floppy Jet Auto Rigger
Written By: Adam Benson
10-25-2018
"""

from maya import cmds

class floppy_jet_builder:
    def __init__(self):
        self.start_engine()

    def get_border_edges(self, obj=None, bb=None, pv=None, d=None):
        threshold = 1.0
        # search_distance is essentially the same as the Block size
        search_distance = d * threshold
        edges = []
        start_side = None
        end_side = None
        is_max = False
        if pv == 'x':
            min_max = [0, 3]
            print 'min_max X'
        elif pv == 'y':
            min_max = [1, 4]
            print 'min_max Y'
        else:
            min_max = [2, 5]
            print 'min_max Z'
        search_min = bb[min_max[0]] + search_distance
        search_max = bb[min_max[1]] - search_distance
        print 'search_min: %s' % search_min
        print 'SEARCH_MAX: %s' % search_max
        if obj:
            print 'obj: %s' % obj
            cmds.select(obj, r=True)
            cmds.selectType(pe=True)
            cmds.polySelectConstraint(m=3, t=0x8000, bo=True)
            cmds.polySelectConstraint(m=3, t=0x8000, pp=3)
            initial_selection = cmds.ls(sl=True)
            print 'initial selection: %s' % initial_selection
            for selection in initial_selection:
                position = cmds.xform(selection, q=True, t=True, ws=True)
                print 'sub_selection position: %s' % position
                search_point = position[min_max[0]]
                print 'search_point: %s' % search_point
                if bb[min_max[0]] < search_point < search_min:
                    print 'Minimum'
                    edges.append(selection)
                    start_side = bb[min_max[0]]
                    end_side = bb[min_max[1]]
                    is_max = False
                elif search_max < search_point < bb[min_max[1]]:
                    print 'Maximum'
                    edges.append(selection)
                    start_side = bb[min_max[1]]
                    end_side = bb[min_max[0]]
                    is_max = True
            cmds.polySelectConstraint(dis=True)
            if edges:
                print 'EDGES: %s' % edges
                cmds.select(edges, r=True)
                cmds.select(obj, tgl=True)
                cmds.selectMode(component=True)
        return edges, start_side, is_max, end_side

    def get_primary_vector(self, bb=None):
        # Returns the longest direction of the bounding box, providing the primary vector
        primary_vector = None
        if bb:
            xMin = bb[0]
            yMin = bb[1]
            zMin = bb[2]
            xMax = bb[3]
            yMax = bb[4]
            zMax = bb[5]

            xDelta = xMax - xMin
            yDelta = yMax - yMin
            zDelta = zMax - zMin
            deltas = {'x': xDelta, 'y': yDelta, 'z': zDelta}
            max_delta = max(deltas.values())
            print 'deltas: %s' % deltas
            print 'max_delta: %s' % max_delta
            primary_vector = [[k for k, v in deltas.items() if v == max_delta][0], max_delta]
            print 'primary_vector: %s' % primary_vector
        return primary_vector

    def get_center(self):
        loop_bb = cmds.xform(q=True, bb=True, ws=True)
        x_center = ((loop_bb[3] - loop_bb[0]) / 2) + loop_bb[0]
        y_center = ((loop_bb[4] - loop_bb[1]) / 2) + loop_bb[1]
        z_center = ((loop_bb[5] - loop_bb[2]) / 2) + loop_bb[2]
        center = [x_center, y_center, z_center]
        print 'center: %s' % center
        return center

    def create_joint_at_point(self, point=None, obj=None, num=1):
        joint = None
        joint_name = '%s_%02d_BND' % (obj, num)
        if point:
            print 'Create a joint at %s' % point
            joint = cmds.joint(n=joint_name, p=point)
        return joint

    def get_edgeloops_and_build(self, edges=None, direction='x', is_max=False, delta=1.0, bb=None):
        threshold = 0.02
        joint_division = 10
        selected_edges = []
        obj_centers = []
        search_distance = None
        if edges:
            for edge in edges:
                selected_edges.append(edge)
            cmds.select(selected_edges, r=True)
            # This center is the "Primary/Initial" center point.  This is where the First-Previous thing gets started.
            center = self.get_center()
            print 'Center: %s' % center
            # obj_centers.append(center)

            if direction == 'x':
                c = 0
                bbMin = bb[0]
                bbMax = bb[3]
                width = bb[5] - bb[2]
                height = bb[4] - bb[1]
            elif direction == 'y':
                c = 1
                bbMin = bb[1]
                bbMax = bb[4]
                width = bb[3] - bb[0]
                height = bb[5] - bb[2]
            else:
                c = 2
                bbMin = bb[2]
                bbMax = bb[5]
                width = bb[3] - bb[0]
                height = bb[4] - bb[1]
            length = bbMax - bbMin
            primary_delta = bbMax - bbMin
            T = (width * height) * threshold
            section_depth = length/joint_division
            start_point = center[c]
            next_point = start_point + section_depth
            # Next I need to collect ALL the edge loops as iteratables.
            # Then, I need to run the center/threshold algorithm for each of those centers.
            # The remaining collection of centers will be where the average centers come from.
            searched_loops = []  # This is r below
            current_selection = selected_edges
            while current_selection not in searched_loops:
                searched_loops.append(current_selection)
                cmds.pickWalk(d='right', type='edgeloop')
                current_selection = []
                new_loop = cmds.ls(sl=True)
                obj_centers.append(self.get_center())
                for sel in new_loop:
                    current_selection.append(sel)
            cmds.select(cl=True)
            for point in obj_centers:
                print point
        #
        #     # --------------------------- From Maya
        #     objs = cmds.ls(sl=True)
        #     for obj in objs:
        #         cmds.selectType(pe=True)
        #         cmds.polySelectConstraint(m=3, t=0x8000, bo=True)
        #         cmds.polySelectConstraint(m=3, t=0x8000, pp=3)
        #         cmds.pickWalk(d='right', type='edgeloop')
        #         p = cmds.ls(sl=True)
        #         # Already have everything above
        #         # Also Already have the q list called selected_edges
        #         q = []
        #         for tp in p:
        #             q.append(tp)
        #         # Ok, so r is basically the list of acceptable edges.  For everything in selected_edges, if it's not in
        #         # r then the loop continues
        #         # So, our r will be something like, searched_loops
        #         r = []
        #         print 'original q: %s' % q
        #         while q not in r:
        #             r.append(q)
        #             cmds.pickWalk(d='right', type='edgeloop')
        #             q = []
        #             p = cmds.ls(sl=True)
        #             for tp in p:
        #                 q.append(tp)
        #             print q
        #         cmds.select(cl=True)
        #         for d in r:
        #             cmds.select(d, tgl=True)
        #         cmds.select(obj, tgl=True)
        #         cmds.selectMode(co=True)
        #     cmds.polySelectConstraint(dis=True)
        #     # -------------------------------------End from maya
        #
        #     print 'First CENTER: %s' % center
        #     # This may be where I need to start injecting the Threshold and other shit from my notes and tests.
        #     # It's also possible that the direction bit is unnecessary with the new algorithm
        #     if is_max and direction == 'x' or direction == 'y':
        #         d = 'left'
        #         neg = True
        #     elif is_max and direction == 'z':
        #         d = 'right'
        #         neg = True
        #     elif not is_max and direction != 'z':
        #         d = 'right'
        #         neg = False
        #     else:
        #         neg = False
        #         d = 'left'
        #     start_search = True
        #     cmds.pickWalk(d=d, type='edgeloop')
        #     # This is where I need to switch my edge/center collection algorithm
        #
        #     while start_search:
        #         cmds.pickWalk(d=d, type='edgeloop')
        #         new_edges = cmds.ls(sl=True)
        #         new_center = self.get_center()
        #         previous = center[c]
        #         new = new_center[c]
        #         if neg:
        #             if not search_distance and new != previous:
        #                 search_distance = (((delta / (new - previous))) ** 2) ** 0.5
        #                 print 'search_distance: %s' % search_distance
        #             if new < (previous - search_distance):
        #                 print '&' * 50
        #                 print 'new point NEG: %s' % new
        #                 print 'previous search distance NEG: %s' % (previous - search_distance)
        #                 print 'previous point NEG: %s' % previous
        #                 print '^' * 50
        #                 selected_edges.append(new_edges)
        #                 center = new_center
        #                 obj_centers.append(new_center)
        #             else:
        #                 print 'NEG - new was not less than the previous search dist: %s | %s' % (new, (previous - search_distance))
        #                 start_search = False
        #         else:
        #             if not search_distance and new != previous:
        #                 search_distance = ((delta / (new - previous)) ** 2) ** 0.5
        #                 print 'search_distance: %s' % search_distance
        #             if new > (previous + search_distance):
        #                 print '&' * 50
        #                 print 'new point: %s' % new
        #                 print 'previous search distance: %s' % (previous + search_distance)
        #                 print 'previous point: %s' % previous
        #                 print '^' * 50
        #                 selected_edges.append(new_edges)
        #                 center = new_center
        #                 obj_centers.append(new_center)
        #             else:
        #                 start_search = False
        return selected_edges, obj_centers

    def create_joints_from_centers(self, centers=None, obj=None):
        joints = []
        if centers:
            num = 1
            for center in centers:
                joint = self.create_joint_at_point(point=center, obj=obj, num=num)
                joints.append(joint)
                num += 1
        return joints

    def start_engine(self):
        selected_objects = cmds.ls(sl=True)
        for obj in selected_objects:
            bb = cmds.xform(obj, q=True, bb=True)
            get_primary_vector = self.get_primary_vector(bb=bb)
            primary_vector = get_primary_vector[0]
            distance = get_primary_vector[1]
            border_edges = self.get_border_edges(obj=obj, bb=bb, pv=primary_vector, d=distance)
            border_edge = border_edges[0]
            starting_point = border_edges[1]
            is_max = border_edges[2]
            end_point = border_edges[3]
            print 'dookie'
            print end_point
            print starting_point
            delta = ((end_point - starting_point) ** 2) ** 0.5
            print 'absolute delta end to start: %s' % delta
            edge_selection = self.get_edgeloops_and_build(edges=border_edge, direction=primary_vector, is_max=is_max,
                                                          delta=delta, bb=bb)
            # print 'Edge Selection: %s' % edge_selection
            cmds.selectMode(component=True)
            cmds.select(cl=True)
            for sel in edge_selection[0]:
                cmds.select(sel, tgl=True)
            centers = edge_selection[1]
            print 'centers: %s' % centers
            cmds.select(cl=True)
            cmds.selectMode(object=True)
            cmds.select(cl=True)
            joints = self.create_joints_from_centers(centers=centers, obj=obj)
            cmds.select(cl=True)
            print 'joints: %s' % joints

            print '=' * 200

if __name__ == '__main__':
    run = floppy_jet_builder()


