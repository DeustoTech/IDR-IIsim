"""Script to generate yearly production of several industries"""

import os
import sys
import csv
from pathlib import Path
from industries.cement import Cement
from industries.steel import Steel

NUTS_CSV_PATH = "nuts_csvs"

industries = {
    "NMM": Cement,
    "CEMENT": Cement,
    "ISI": Steel,
    "STEEL": Steel,
}


def process_csv(dir_path, csv_file, industry):
    output_csv = "OUTPUT_" + csv_file
    output_folder = os.path.join(dir_path, "outputs")
    results = []
    nuts = {}
    with open(
        os.path.join(dir_path, csv_file), mode="r", encoding="utf-8"
    ) as input_file:
        csv_reader = csv.reader(input_file)
        header = next(csv_reader)

        # Generate header
        prod = industry(1)
        result_header = header[0:2]
        result_header.append("Year")
        result_header.extend(prod.csv_header())
        results.append(result_header)
        # Generate rows
        for row in csv_reader:
            nut_scode = row[0]
            nut_slevel = row[1]
            code = nut_scode[:2]
            if code not in nuts and nut_slevel and nut_slevel in "0123":
                nuts[code] = {"0": 0, "1": 0, "2": 0, "3": 0}
            # print(nut_scode, code, row[1], nut_slevel, nuts[code])
            for index in range(2, len(row)):
                year = header[index]
                value = row[index]
                if value:
                    kton = float(value)
                    if nut_slevel and nut_slevel in "0123":
                        nuts[code][nut_slevel] += kton
                    prod = industry(kton)
                    result = [nut_scode, nut_slevel, year]
                    result.extend(prod.csv_row())
                    results.append(result)

    # Check data
    is_data_ok = True
    for code in nuts:
        print(f"{code}:", end="\t")
        for i in range(1, 4):
            if abs(nuts[code]["0"] - nuts[code][str(i)]) < 0.1:
                print("OK".ljust(13), end="\t")
            else:
                print(
                    "DIFFERENT!!",
                    end="\t",
                )
                is_data_ok = False
        print()

    should_generate_output = is_data_ok
    if not is_data_ok:
        print("The input data has some discrpencies")
        should_generate_output = (
            input(
                "Should we proceed to generate the output file? (y/N) "
            ).lower()
            == "y"
        )

    if should_generate_output:
        with open(
            os.path.join(output_folder, output_csv),
            mode="w",
            encoding="utf-8",
            newline="",
        ) as output_file:
            csv_writer = csv.writer(output_file)
            for row in results:
                csv_writer.writerow(row)
        print(f"File '{output_csv}' generated succesfully.")


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Uso: python verificar_nuts.py")
    else:
        os.makedirs(os.path.join(NUTS_CSV_PATH, "outputs"), exist_ok=True)
        for ruta_csv in Path(NUTS_CSV_PATH).glob("*.csv"):
            folder, filename = os.path.split(ruta_csv)
            ind = filename.split("_")[0]
            process_csv(folder, filename, industries[ind.upper()])
