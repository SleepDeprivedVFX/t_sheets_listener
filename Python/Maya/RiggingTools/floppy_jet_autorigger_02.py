"""
Floppy Jet Auto Rigger
Written By: Adam Benson
10-25-2018
"""

from maya import cmds


class floppy_jet_builder:
    def __init__(self, threshold=0.02, joints=10, buffer_size=0.5):
        self.start_engine(threshold=threshold, joints=joints, buffer_size=buffer_size)

    def select_edge_loops(self, obj=None):
        select_edges = []
        if obj:
            cmds.select(obj, r=True)
            cmds.selectType(pe=True)
            cmds.polySelectConstraint(m=3, t=0x8000, bo=True)
            cmds.polySelectConstraint(m=3, t=0x8000, pp=3)
            cmds.pickWalk(d='right', type='edgeloop')
            selection = cmds.ls(sl=True)
            queue = []
            for edge in selection:
                queue.append(edge)

            while queue not in select_edges:
                select_edges.append(queue)
                cmds.pickWalk(d='right', type='edgeloop')
                del queue
                queue = []
                new_selection = cmds.ls(sl=True)
                for sel in new_selection:
                    queue.append(sel)
            cmds.select(cl=True)
            for edge_loop in select_edges:
                cmds.select(edge_loop, tgl=True)
            cmds.select(obj, tgl=True)
            cmds.selectMode(co=True)
        return select_edges

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

    def width_height(self, direction='x', bb=None):
        width_height = {}
        if bb:
            if direction == 'x':
                width = bb[5] - bb[2]
                height = bb[4] - bb[1]
            elif direction == 'y':
                width = bb[3] - bb[0]
                height = bb[5] - bb[2]
            else:
                width = bb[3] - bb[0]
                height = bb[4] - bb[1]
            width_height['width'] = width
            width_height['height'] = height
        return width_height

    def get_center(self):
        loop_bb = cmds.xform(q=True, bb=True, ws=True)
        x_center = ((loop_bb[3] - loop_bb[0]) / 2) + loop_bb[0]
        y_center = ((loop_bb[4] - loop_bb[1]) / 2) + loop_bb[1]
        z_center = ((loop_bb[5] - loop_bb[2]) / 2) + loop_bb[2]
        center = [x_center, y_center, z_center]
        print 'center: %s' % center
        return center

    def centers(self, selected_edges=None, threshold=0.0):
        centers = []
        if selected_edges:
            cmds.select(cl=True)
            for loop in selected_edges:
                cmds.select(loop, r=True)
                local_bb = self.get_center()
                centers.append(local_bb)
        return centers

    def find_local_centers(self, min=0.0, max=1.0, threshold=0.0, centers=None, bufferMin=-1.0, bufferMax=2.0,
                           vector=0):
        local_centers = []
        in_buffer = []
        in_bounds = []
        if centers:
            # There are a list of center points: [[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]]
            for center in centers:
                local_averages = []
                # The vector is an integer value that selects the input 0 = x, 1 = y, 2 = z
                # Thus:
                # vector = 2
                # center[vector] = center[2] = 1.0
                # This gives us the position along the bounding box length
                axis_point = center[vector]

                # Now, if it within the buffer zones, we add it to the buffer list
                # If it is within the bounds of the slice being analyzed, then it's added the main list
                if min < axis_point < max:
                    in_bounds.append(center)
                elif bufferMin < axis_point < min or max < axis_point < bufferMax:
                    in_buffer.append(center)
                if not in_bounds:
                    in_bounds += in_buffer
                # So, if we have points in the range of our search area...
                if in_bounds:
                    # I set the "zero distance" point for the difference equation
                    x1 = center[0]
                    y1 = center[1]
                    z1 = center[2]
                    # Now, even though I'm already looping through the list, I still have to loop back through the same
                    # list, because I am comparing it's current point to points all around itself.
                    # If those points are within the search threshold, then they should be added to the primary search
                    # list.  That list will have only one center per slice, getting the average from this list.
                    for compare in centers:
                        if compare != center:
                            in_threshold = False
                            x2 = compare[0]
                            y2 = compare[1]
                            z2 = compare[2]
                            point_dist = ((x2 - x1) ** 3) + ((y2 - y1) ** 3) + ((z2 - z1) ** 3)
                            point_dist **= 2
                            point_dist **= 0.5
                            point_dist **= 0.3333333333333
                            if point_dist < threshold:
                                in_threshold = True
                            if in_threshold and compare not in local_averages:
                                local_averages.append(compare)
                    if local_averages:
                        if center not in local_averages:
                            local_averages.append(center)
                        # print 'local_averages: %s' % local_averages

                        # Time to sort through the locals and find the one true center.
                        avg_x = 0.0
                        avg_y = 0.0
                        avg_z = 0.0
                        point_count = len(local_averages)
                        for avg in local_averages:
                            avg_x += avg[0]
                            avg_y += avg[1]
                            avg_z += avg[2]
                        x = avg_x / point_count
                        y = avg_y / point_count
                        z = avg_z / point_count
                        new_center = [x, y, z]
                        if new_center not in local_centers:
                            # print 'new_center: %s' % new_center
                            local_centers.append(new_center)
                else:
                    print 'NOT ENOUGH POINTS FOUND FOR SOME FUCKIN REASON'

            if local_centers:
                if len(local_centers) > 1:
                    local_centers = self.find_local_centers(min=min, max=max, threshold=threshold,
                                                            centers=local_centers, bufferMin=bufferMin,
                                                            bufferMax=bufferMax, vector=vector)
                print '=' * 200
                # print 'local_centers: %s' % local_centers
                print 'From %s' % min
                # for avg in local_centers:
                #     print 'local average collection: %s' % avg
                print 'To %s' % max
                print 'At Threshold %s' % threshold
            # else:
            #     local_centers = self.find_local_centers(min=min, max=max, threshold=threshold, centers=in_buffer,
            #                                             bufferMin=bufferMin, bufferMax=bufferMax, vector=vector)
        return local_centers

    def start_engine(self, threshold=0.02, joints=1, buffer_size=0.5):
        selected_objects = cmds.ls(sl=True)
        for obj in selected_objects:
            """
            So, I need to get the bounding box length, threshold and other settings before doint
            all these freaking calculations.
            """
            cmds.select(obj, r=True)
            bb = cmds.xform(q=True, bb=True)
            primary_vector = self.get_primary_vector(bb=bb)
            directional_axis = primary_vector[0]
            total_length = primary_vector[1]
            section_depth = total_length / joints
            width_height = self.width_height(direction=directional_axis, bb=bb)
            width = width_height['width']
            height = width_height['height']
            Threshold = (width * height) * threshold
            print 'Threshold: %s' % Threshold

            selected_edges = self.select_edge_loops(obj=obj)
            print 'primary vector: %s' % primary_vector
            print 'selected_eges: %s' % selected_edges
            centers = self.centers(selected_edges=selected_edges, threshold=Threshold)
            print 'returned centers: %s' % centers

            """
            Now that I have a collection of center points, it is time to break the area into sections and begin
            scanning both the internal and buffer areas for sectional center points.
            Once I have the center points for a given section, then I can start the average, thresholding to find the
            actual center points for each joint section.
            Then you can create the joints....
            """

            if directional_axis == 'x':
                # c is the center index for the length point, given (x, y, z)
                c = 0
                Min = bb[0]
                Max = bb[3]
            elif directional_axis == 'y':
                c = 1
                Min = bb[1]
                Max = bb[4]
            else:
                c = 2
                Min = bb[2]
                Max = bb[5]

            start = Min
            end = Min + section_depth
            block = 1
            while end <= Max:
                print 'BLOCK %i' % block
                bufferMin = start - (section_depth * buffer_size)
                bufferMax = end + (section_depth * buffer_size)
                local_centers = self.find_local_centers(min=start, max=end, threshold=Threshold, centers=centers,
                                                        bufferMin=bufferMin, bufferMax=bufferMax, vector=c)
                print 'LOCAL CENTERS BLOCK %i' % block
                print local_centers
                if local_centers:
                    averaged_center_point = local_centers[0]
                    if averaged_center_point:
                        cmds.spaceLocator(p=averaged_center_point)
                start = end
                end += section_depth
                block += 1
                print '^' * 200


if __name__ == '__main__':
    run = floppy_jet_builder(threshold=0.2, joints=10, buffer_size=0.5)

