class Tracker:
    def __init__(self, compare_f, track_ttl):
        """
        Tracker initialization
        :param compare_f: function to compare boxes
        :param track_ttl: Number of updates to keep not tracked box
        """
        # Dict of form 'track id : box'
        self.tracks = {}
        self.next_id = 1

        # Thresholds for graduate tracks update
        self.update_stages = [0.9, 0.8, 0.7, 0.6, 0.5, 0.2, 0]
        self.compare = compare_f
        self.track_default_ttl = track_ttl

    def update_tracks(self, new_boxes):
        """
        Update tracks based on set of boxes, create new ones and delete old ones
        :param new_boxes: List of dicts with keys 'leftup' and 'rightdown', each having 'x' and 'y' coordinates
        """

        # Compare all pairs of tracks and boxes with each other
        comp_matrix = {}
        for track_id in self.tracks.keys():
            comp_matrix[track_id] = {}
            for box_id in range(len(new_boxes)):
                comp_matrix[track_id][box_id] = self.compare(self.tracks[track_id], new_boxes[box_id])

        untracked_boxes = list(range(len(new_boxes)))

        # Update tracks with most matching boxes
        # Start from high threshold and end on small one
        for threshold in self.update_stages:
            # Go through tracks that are not updated yet
            tracks_to_update = list(comp_matrix.keys())
            for track_id in tracks_to_update:

                # Stop search if there is no boxes left
                if len(comp_matrix[track_id].keys()) == 0:
                    break

                # Find box with best comparison score
                best_box_id = max(comp_matrix[track_id], key=comp_matrix[track_id].get)

                # Update tracker only if score passes the threshold
                if comp_matrix[track_id][best_box_id] > threshold:
                    # Update track
                    self.tracks[track_id]['leftup']['x'] = new_boxes[best_box_id]['leftup']['x']
                    self.tracks[track_id]['leftup']['y'] = new_boxes[best_box_id]['leftup']['y']
                    self.tracks[track_id]['rightdown']['x'] = new_boxes[best_box_id]['rightdown']['x']
                    self.tracks[track_id]['rightdown']['y'] = new_boxes[best_box_id]['rightdown']['y']
                    # Reset track ttl
                    self.tracks[track_id]['ttl'] = self.track_default_ttl

                    # Delete box from matrix (Column)
                    for key in comp_matrix.keys():
                        comp_matrix[key].pop(best_box_id)

                    # Delete box from untracked ones
                    untracked_boxes.remove(best_box_id)

                    # Delete track from matrix (Row)
                    comp_matrix.pop(track_id)


        # Create new tracks from untracked boxes
        for box_id in untracked_boxes:
            self.tracks[self.next_id] = {
                'leftup': {
                    'x': new_boxes[box_id]['leftup']['x'],
                    'y': new_boxes[box_id]['leftup']['y']
                },
                'rightdown': {
                    'x': new_boxes[box_id]['rightdown']['x'],
                    'y': new_boxes[box_id]['rightdown']['y']
                },
                'ttl': self.track_default_ttl,
            }
            self.next_id += 1

        # Decrease ttl of left tracks and remove too old ones
        for track_id in comp_matrix.keys():
            self.tracks[track_id]['ttl'] -= 1
            if self.tracks[track_id]['ttl'] == 0:
                self.tracks.pop(track_id)

