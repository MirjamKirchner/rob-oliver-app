import os
import pandas as pd
import numpy as np
import datetime
import boto3
import botocore
import io

S3_BUCKET = "rob-oliver"
KEY = "data/deployment/rob.csv"


def _load_rob():
    """
    Loads the data to be displayed in the app.
    :return: (pd.DataFrame) a data frame containing information about seals admitted to the Seehundstation
    Friedrichskoog
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
            print(error)
        raise
    except:
        print("An unexpected exception has occurred.")
        raise
    else:
        df_rob[
            [
                "Long",
                "Lat",
                "Einlieferungsdatum",
                "Erstellt_am",
                "Sys_aktualisiert_am",
                "Sys_geloescht",
            ]
        ] = df_rob[
            [
                "Long",
                "Lat",
                "Einlieferungsdatum",
                "Erstellt_am",
                "Sys_aktualisiert_am",
                "Sys_geloescht",
            ]
        ].astype(
            {
                "Long": "float64",
                "Lat": "float64",
                "Einlieferungsdatum": "datetime64[ns]",
                "Erstellt_am": "datetime64[ns]",
                "Sys_aktualisiert_am": "datetime64[ns]",
                "Sys_geloescht": "int32",
            }
        )
        return df_rob


DF_ROB = _load_rob()


def create_part_to_whole(
    max_date: datetime = pd.to_datetime("today"),
    min_date: datetime = pd.to_datetime("1990-04-30"),
):
    """
    Computes the parts to whole of seals in rehabilitation, released, and died within the time range
    [min_date, max_date).
    :param max_date: (datetime) maximal date
    :param min_date: (datetime) minial date
    :return: (pd.DataFrame) temporally filtered parts to whole (in rehabilitation, released, died)
    """
    df_time_slice = DF_ROB.loc[
        (DF_ROB["Einlieferungsdatum"] >= min_date) & (DF_ROB["Erstellt_am"] < max_date),
        ["Erstellt_am", "Sys_id", "Sys_geloescht"],
    ]
    df_latest_by_id = (
        df_time_slice.set_index(pd.DatetimeIndex(df_time_slice["Erstellt_am"]))
        .groupby(["Sys_id"])
        .last()
    )
    return pd.merge(
        df_latest_by_id,
        DF_ROB,
        how="left",
        on=["Erstellt_am", "Sys_id", "Sys_geloescht"],
    )["Aktuell"].value_counts()


def create_time_series(
    max_date: datetime = pd.to_datetime("today"),
    min_date: datetime = pd.to_datetime("1990-04-30"),
):
    """
    Computes the weekly count of seals admitted to the Seehundstation Friedsrichskoog within the time range
    [min_date, max_date).
    :param max_date: (datetime) maximal date
    :param min_date: (datetime) minial date
    :return: (pd.DataFrame) temporally filtered time series of weekly counts of admitted seals
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
    :param max_date: (datetime) maximal date
    :param min_date: (datetime) minial date
    :return: (pd.DataFrame) temporally filtered counts of admitted seals for different finding places
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
    )  # Some animals have an unkown finding place. Therefore, the total count here is below the actual.
    return df_bubbles


def get_marks(min_date, max_date):
    """
    Convert DateTimeIndex to a dict that maps epoch to str
    :param min_date: (int) minimal epoch
    :param max_date: (int) maximal epoch
    :return: (dict) format is {
            1270080000: "04-2010",
            1235865600: "03-2009",
             ...
        }
    """
    months = (
        pd.date_range(min_date, max_date, freq="MS")
        .to_period("M")
        .unique()
        .sort_values()
    )
    epochs = months.to_timestamp().astype(np.int64) // 10**9
    strings = months.strftime("%m-%Y")
    return dict(zip(epochs, strings))


if __name__ == "__main__":
    b = create_bubbles()
    t = create_time_series()
    print("Sanity checks")
    print(DF_ROB["Sys_id"].unique().size)
    print(b["Anzahl"].sum())
    print(t["Anzahl"].sum())
