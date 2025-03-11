import plotly.graph_objects as go


def arrange_fig(fig: go.Figure):
    # Configure the graph's title and axis labels
    fig.update_layout(
        height=600,
        width=800,
        template="plotly_white",
        title_font=dict(size=32),
        xaxis_title_font=dict(family="Times New Roman", size=32, color="black"),
        yaxis_title_font=dict(family="Times New Roman", size=32, color="black"),
        xaxis=dict(
            tickfont=dict(family="Times New Roman", size=22, color="black"),
            title_standoff=10,
            ticklen=10,  # 目盛線の長さ
            tickwidth=2,  # 目盛線の太さ
            tickcolor="black",  # 目盛線の色
            ticks="outside",  # 内側に目盛線を表示
        ),
        yaxis=dict(
            tickfont=dict(family="Times New Roman", size=22, color="black"),
            title_standoff=5,
            tickangle=0,  # 角度を調整（必要であれば変更）
            automargin=True,  # 自動的にラベルの間隔を調整
            ticklen=10,  # 目盛線の長さ
            tickwidth=2,  # 目盛線の太さ
            tickcolor="black",  # 目盛線の色
            ticks="outside",  # 内側に目盛線を表示
        ),
        showlegend=True,
        legend=dict(
            x=0.95,
            y=0.6,
            xanchor="right",
            yanchor="bottom",
            font=dict(family="Times New Roman", size=20, color="black"),
        ),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color="black",
                    width=2,
                ),
                fillcolor="rgba(0,0,0,0)",
            )
        ],
        margin=dict(l=100, r=100, b=100, t=100),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


class ResultGrahpGenerator:
    @classmethod
    def plot_loss_comparison(cls, losss_dict):
        fig = go.Figure()

        # 各最適化手法の損失をプロット
        for key, loss_values in losss_dict.items():
            fig.add_trace(go.Scatter(y=loss_values, mode="lines", name=key))

        # レイアウト設定
        fig.update_layout(
            title="Loss Comparison for Different Optimizers",
            xaxis_title="Epochs",
            yaxis_title="Loss",
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            template="plotly_white",
        )

        # arrange_fig を適用（定義されている場合）
        if "arrange_fig" in globals():
            fig = arrange_fig(fig)

        return fig
