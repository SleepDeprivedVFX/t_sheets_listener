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
        threshold = 0.1
        search_distance = d * threshold
        edges = []
        start_side = None
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
            cmds.select(obj, r=True)
            cmds.selectType(pe=True)
            cmds.polySelectConstraint(m=3, t=0x8000, bo=True)
            cmds.polySelectConstraint(m=3, t=0x8000, pp=3)
            initial_selection = cmds.ls(sl=True)
            for selection in initial_selection:
                position = cmds.xform(selection, q=True, t=True, ws=True)
                search_point = position[min_max[0]]
                if bb[min_max[0]] < search_point < search_min:
                    edges.append(selection)
                    start_side = bb[min_max[0]]
                    end_side = bb[min_max[1]]
                    is_max = False
                elif search_max < search_point < bb[min_max[1]]:
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
        loop_bb = cmds.xform(q=True, bb=True)
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

    def get_edgeloops_and_build(self, edges=None, direction='x', is_max=False, delta=1.0):
        selected_edges = []
        obj_centers = []
        search_distance = None
        if edges:
            for edge in edges:
                selected_edges.append(edge)
            cmds.select(edges, r=True)
            center = self.get_center()
            print center
            # obj_centers.append(center)

            if direction == 'x':
                c = 0
            elif direction == 'y':
                c = 1
            else:
                c = 2

            print 'First CENTER: %s' % center
            if is_max and direction == 'x' or direction == 'y':
                d = 'left'
                neg = True
            elif is_max and direction == 'z':
                d = 'right'
                neg = True
            elif not is_max and direction != 'z':
                d = 'right'
                neg = False
            else:
                neg = False
                d = 'left'
            start_search = True
            cmds.pickWalk(d=d, type='edgeloop')
            while start_search:
                cmds.pickWalk(d=d, type='edgeloop')
                new_edges = cmds.ls(sl=True)
                new_center = self.get_center()
                previous = center[c]
                new = new_center[c]
                if neg:
                    if not search_distance and new != previous:
                        search_distance = (((delta / (new - previous))) ** 2) ** 0.5
                        print 'search_distance: %s' % search_distance
                    if new < (previous - search_distance):
                        print '&' * 50
                        print new
                        print (previous - search_distance)
                        print previous
                        print '^' * 50
                        selected_edges.append(new_edges)
                        center = new_center
                        obj_centers.append(new_center)
                    else:
                        start_search = False
                else:
                    if not search_distance and new != previous:
                        search_distance = ((delta / (new - previous)) ** 2) ** 0.5
                        print 'search_distance: %s' % search_distance
                    if new > (previous + search_distance):
                        print '&' * 50
                        print new
                        print (previous + search_distance)
                        print previous
                        print '^' * 50
                        selected_edges.append(new_edges)
                        center = new_center
                        obj_centers.append(new_center)
                    else:
                        start_search = False
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
            delta = ((end_point - starting_point) ** 2) ** 0.5
            print delta
            edge_selection = self.get_edgeloops_and_build(edges=border_edge, direction=primary_vector, is_max=is_max,
                                                          delta=delta)
            print edge_selection
            cmds.select(cl=True)
            for sel in edge_selection[0]:
                cmds.select(sel, tgl=True)
            cmds.selectMode(component=True)
            centers = edge_selection[1]
            print centers
            cmds.selectMode(object=True)
            cmds.select(cl=True)
            joints = self.create_joints_from_centers(centers=centers, obj=obj)
            cmds.select(cl=True)
            print joints

            print '=' * 200

if __name__ == '__main__':
    run = floppy_jet_builder()


