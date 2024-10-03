import panel as pn

from great_tables import GT, html
from great_tables.data import sza

# ref: https://discourse.holoviz.org/t/great-tables/6960

pn.extension()


@pn.cache
def get_sza_pivot():
    return (
        sza.assign(tst_int=lambda df_: df_.tst.astype(int))
        .query("latitude == '20' and tst_int <= 1200")
        .drop(["latitude", "tst_int"], axis=1)
        .dropna()
        .pivot(values=["sza"], index=["month"], columns=["tst"])
        .droplevel(0, axis=1)
        .reindex(
            [
                "jan",
                "feb",
                "mar",
                "apr",
                "may",
                "jun",
                "jul",
                "aug",
                "sep",
                "oct",
                "nov",
                "dec",
            ],
            axis=0,
        )
        .reset_index(names="month")
    )


def get_table() -> GT:
    return (
        GT(get_sza_pivot(), rowname_col="month")
        .data_color(
            domain=[90, 0],
            palette=["rebeccapurple", "white", "orange"],
            na_color="white",
        )
        .tab_header(
            title="Solar Zenith Angles from 05:30 to 12:00",
            subtitle=html("Average monthly values at latitude of 20&deg;N."),
        )
        .sub_missing(missing_text="")
    )


main_content = get_table()

pn.template.FastListTemplate(
    site="Panel",
    title="Great Tables",
    main=[main_content],
    main_layout=None,
    accent="#70409f",
).servable()
