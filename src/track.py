import ast
import numpy as np
import pandas


def load_track_csv(csv_path: str):
    data = pandas.read_csv(csv_path)
    tracks = []
    line = 1

    for v in data.values:
        line += 1
        track = Track()
        track.line_no = line
        track.id = v[0]
        track.name = v[1]
        track.popularity = v[2]
        track.duration_ms = v[3]
        track.explicit = v[4]
        track.artists = ast.literal_eval(v[5])
        track.id_artists = ast.literal_eval(v[6])
        track.release_date = v[7]
        track.key = v[10]
        track.mode = v[12]
        track.time_signature = v[19]
        track.attribute_vec = [v[8], v[9], v[11]]
        track.attribute_vec.extend(v[13:19])
        tracks.append(track)

    return data, tracks

class Track:
    line_no: int
    id: str
    name: str
    popularity: float
    duration_ms: int
    explicit: bool
    artists: []
    id_artists: []
    release_date: str
    key: float
    mode: int
    time_signature: int
    attribute_vec: []

    def normalize_vec(self, min_vec, max_vec):
        for i in range(0, len(self.attribute_vec)):
            if max_vec[i] - min_vec[i] == 0:
                continue

            self.attribute_vec[i] = (self.attribute_vec[i] - min_vec[i])/(max_vec[i] - min_vec[i])

    def as_np_vec(self):
        return np.array(self.attribute_vec)
