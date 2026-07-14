"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import zipfile
import glob
import pandas as pd
import os
from datetime import datetime

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    zip_folder = 'files/input/*'

    dataframes = []

    for zip_path in glob.glob(zip_folder):
        with zipfile.ZipFile(zip_path, 'r') as z:
            csv_filename = z.namelist()[0]
            with z.open(csv_filename) as csv_file:
                df = pd.read_csv(csv_file)
                dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    client_df = pd.DataFrame()

    client_df["client_id"] = combined_df["client_id"]
    client_df["age"] = combined_df["age"]
    client_df["job"] = combined_df["job"].str.replace(".", "").str.replace("-", "_")
    client_df["marital"] = combined_df["marital"]
    client_df["education"] = combined_df["education"].str.replace(".", "_").str.replace("unknown","pd.NA")
    client_df["credit_default"] = combined_df["credit_default"].apply(lambda x: x.replace("yes", "1") if "yes" in x else "0")
    client_df["mortgage"] = combined_df["mortgage"].apply(lambda x: x.replace("yes", "1") if "yes" in x else "0")

    campaign_df = pd.DataFrame()

    campaign_df["client_id"] = combined_df["client_id"]
    campaign_df["number_contacts"] = combined_df["number_contacts"]
    campaign_df["contact_duration"] = combined_df["contact_duration"]
    campaign_df["previous_campaign_contacts"] = combined_df["previous_campaign_contacts"]
    campaign_df["previous_outcome"] = combined_df["previous_outcome"].apply(lambda x: x.replace("success", "1") if "success" in x else "0")
    campaign_df["campaign_outcome"] = combined_df["campaign_outcome"].apply(lambda x: x.replace("yes", "1") if "yes" in x else "0")
    campaign_df["last_contact_date"] = combined_df.apply(lambda row: datetime.strptime(f"2022-{row['month']}-{row['day']}", "%Y-%b-%d").strftime("%Y-%m-%d"), axis=1)
    economics_df = pd.DataFrame()

    economics_df["client_id"] = combined_df["client_id"]
    economics_df["cons_price_idx"] = combined_df["cons_price_idx"]
    economics_df["euribor_three_months"] = combined_df["euribor_three_months"]

    output_folder = "files/output"

    os.makedirs(output_folder, exist_ok=True)

    client_df.to_csv(os.path.join(output_folder, 'client.csv'), index=False)
    campaign_df.to_csv(os.path.join(output_folder, 'campaign.csv'), index=False)
    economics_df.to_csv(os.path.join(output_folder, 'economics.csv'), index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()