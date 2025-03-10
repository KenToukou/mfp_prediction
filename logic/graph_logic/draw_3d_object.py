import plotly.graph_objects as go


class GraphCreator:
    @classmethod
    def draw_3d_object(cls, processed_object):
        fig = go.Figure(
            data=[
                go.Mesh3d(
                    x=processed_object.vertices[:, 0],
                    y=processed_object.vertices[:, 1],
                    z=processed_object.vertices[:, 2],
                    i=processed_object.faces[:, 0],
                    j=processed_object.faces[:, 1],
                    k=processed_object.faces[:, 2],
                    opacity=0.5,  # メッシュの透過度。適宜変更可能
                    color="lightblue",  # メッシュの色。お好みで変更してください
                    flatshading=True,  # 面を平坦にシェーディングするかどうか
                )
            ]
        )

        fig.update_layout(
            scene=dict(aspectmode="data"), title="Trimesh Object Visualization"
        )
        fig.show()
