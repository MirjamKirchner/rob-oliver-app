import pandas as pd
import datetime
import boto3
import botocore
import io

S3_BUCKET = "rob-oliver"
KEY = "data/deployment/rob.csv"


def _load_rob() -> pd.DataFrame:
    """
    Loads the data to be displayed in the app.

    Returns
    -------
    A `pandas DataFrame` containing information about seals admitted to the Seehundstation Friedrichskoog
    """
    try:
        # The S3-bucket grants read rights to the public, so we do not need to provide credentials
        config = botocore.client.Config(signature_version=botocore.UNSIGNED)
        s3 = boto3.client("s3", config=config)
        rob_obj = s3.get_object(Bucket=S3_BUCKET, Key=KEY)
        df_rob = pd.read_csv(io.BytesIO(rob_obj["Body"].read()))
    except botocore.exceptions.ClientError as error:
        if error.response["Error"]["Code"] == "NoSuchKey":
            print(
                f"The key '{KEY}' you are trying to access in AWS-S3-bucket {S3_BUCKET} does not exist."
            )
        elif error.response["Error"]["Code"] == "AccessDenied":
            print(
                f"The access to key '{KEY}' in AWS-S3-bucket {S3_BUCKET} is denied. It could be that the key does not"
                f" exist."
            )
        else:
            print("An unexpected exception has occurred.")
            print(error)
        raise
    except:
        print("An unexpected exception has occurred.")
        raise
    else:
        df_rob[
            ["Long", "Lat", "Einlieferungsdatum", "Erstellt_am", "Sys_aktualisiert_am"]
        ] = df_rob[
            ["Long", "Lat", "Einlieferungsdatum", "Erstellt_am", "Sys_aktualisiert_am"]
        ].astype(
            {
                "Long": "float64",
                "Lat": "float64",
                "Einlieferungsdatum": "datetime64[ns]",
                "Erstellt_am": "datetime64[ns]",
                "Sys_aktualisiert_am": "datetime64[ns]",
            }
        )
        return df_rob[df_rob["Fundort"] != "Unknown"]


DF_ROB = _load_rob()


def create_part_to_whole(
    max_date: datetime = pd.to_datetime("today"),
    min_date: datetime = pd.to_datetime("1990-04-30"),
):
    """
    Computes the parts to whole of seals in rehabilitation, released, and died within the time range
    [min_date, max_date).

    Parameters
    ----------
    max_date
        maximal date.

    min_date
        minimal date.

    Returns
    -------
    A `pandas DataFrame` describing temporally filtered parts to whole (in rehabilitation, released, died).
    """
    df_time_slice = DF_ROB.loc[
        (DF_ROB["Einlieferungsdatum"] >= min_date) & (DF_ROB["Erstellt_am"] < max_date),
        ["Erstellt_am", "Sys_id"],
    ]
    df_latest_by_id = (
        df_time_slice.sort_values(by=["Sys_id", "Erstellt_am"])
        .groupby(["Sys_id"])
        .last()
    )
    return pd.merge(
        df_latest_by_id,
        DF_ROB,
        how="left",
        on=["Erstellt_am", "Sys_id"],
    )["Aktuell"].value_counts()


def create_time_series(
    max_date: datetime = pd.to_datetime("today"),
    min_date: datetime = pd.to_datetime("1990-04-30"),
):
    """
    Computes the weekly count of seals admitted to the Seehundstation Friedsrichskoog within the time range
    [min_date, max_date).

    Parameters
    ----------
    max_date
        maximal date.

    min_date
        minial date.

    Returns
    -------
    A `pandas DataFrame` describing temporally filtered time series of weekly counts of admitted seals.
    """
    df_time_series = (
        DF_ROB[["Sys_id", "Einlieferungsdatum", "Tierart"]]
        .drop_duplicates()
        .groupby(
            ["Tierart", pd.Grouper(key="Einlieferungsdatum", axis=0, freq="W-MON")]
        )
        .count()
        .reset_index()
        .rename(
            columns={"Einlieferungsdatum": "Einlieferungswoche", "Sys_id": "Anzahl"}
        )
    )
    return df_time_series[
        (df_time_series["Einlieferungswoche"] >= min_date)
        & (df_time_series["Einlieferungswoche"] < max_date)
    ]


def create_bubbles(
    max_date: datetime = pd.to_datetime("today"),
    min_date: datetime = pd.to_datetime("1990-04-30"),
):
    """
    Computes the count of seals admitted to the Seehundstation Friedrichskoog for different finding places within the
    time range [min_date, max_date).

    Parameters
    ----------
    max_date
        maximal date.

    min_date
        minimal date.

    Returns
    -------
    A `pandas DataFrame` describing temporally filtered counts of admitted seals for different finding places.
    """
    df_bubbles = DF_ROB[["Sys_id", "Einlieferungsdatum", "Fundort", "Long", "Lat"]]
    df_bubbles = df_bubbles[
        (df_bubbles["Einlieferungsdatum"] >= min_date)
        & (df_bubbles["Einlieferungsdatum"] < max_date)
    ].drop(columns=["Einlieferungsdatum"])
    df_bubbles = (
        df_bubbles.drop_duplicates()
        .groupby(["Fundort", "Long", "Lat"])
        .count()
        .reset_index()
        .rename(columns={"Sys_id": "Anzahl"})
    )
    return df_bubbles


if __name__ == "__main__":
    b = create_bubbles()
    t = create_time_series()
    print("Sanity checks")
    print(DF_ROB["Sys_id"].unique().size)
    print(b["Anzahl"].sum())
    print(t["Anzahl"].sum())
