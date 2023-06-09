matlab_colors = [
    '#0072BD', '#D95319', '#EDB120', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F'
]

# Constants factors
margin_inches = 1/16
ppi = 300
default_ppi = 96
scale = ppi / default_ppi

width_inches = 3.5

font_size = scale * 8.25
margin = margin_inches * ppi


def paper_style(aspect_ratio=2/3):
    height_inches = aspect_ratio * 3.5
    width = (width_inches - margin_inches) * ppi
    height = (height_inches - margin_inches) * ppi

    return dict(
        width=width,
        height=height,
        title=dict(
            x=0.5
        ),
        xaxis=dict(
            ticks="inside",
        ),
        yaxis=dict(
            ticks="inside",
        ),
        template="simple_white",
        font=dict(
            family="Linux Biolinum O",
            size=font_size
        ),
        legend=dict(
            font=dict(
                family="Linux Biolinum O",
                size=font_size
            ),
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=margin, r=margin, t=6*margin, b=margin)
    )
