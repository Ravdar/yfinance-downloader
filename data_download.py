import yfinance as yf
import os
import pandas as pd


class DataDownload:
    def __init__(self, entry_dir, dest_folder):
        self.entry_dir = entry_dir
        self.dest_folder = dest_folder.replace("/", "\\")
        self.x = 1

    def csv_data(self, checkbox, status):
        self.checkbox = checkbox
        self.status = status
        for ticker in self.entry_dir:
            self.new_data = yf.download(
                tickers=ticker["Ticker"],
                period=ticker["Period"],
                interval=ticker["Interval"],
            )
            self.status.configure(text=f"{self.x}/{len(self.entry_dir)}...")
            print(self.x)
            self.x += 1
            self.path = (
                f'{self.dest_folder}\\{ticker["Ticker"]}\\{ticker["Interval"]}\\CSV RAW'
            )
            #  If there is no old data downloaded before
            if not os.path.exists(self.path):
                os.makedirs(self.path)
                self.new_data.to_csv(f'{self.path}\\{ticker["Ticker"]}', index=True)
                self.new_data_csv = pd.read_csv(f'{self.path}\\{ticker["Ticker"]}')
                #  Deleting time zone from "Datetime" column
                r = 0
                if "Datetime" in self.new_data_csv.columns:
                    for v in self.new_data_csv["Datetime"]:
                        self.new_data_csv.loc[r, "Datetime"] = v[:19]
                        r += 1
            #  If this set of data was downloaded before (there is older data)
            else:

                self.old_data = pd.read_csv(f'{self.path}\\{ticker["Ticker"]}')
                self.old_data = self.old_data.drop_duplicates()
                self.new_data.to_csv(f'{self.path}\\{ticker["Ticker"]} new', index=True)
                self.new_data_csv = pd.read_csv(f'{self.path}\\{ticker["Ticker"]} new')
                self.merged_data = pd.concat(
                    [self.old_data, self.new_data_csv],
                    axis=0,
                    ignore_index=True,
                    join="outer",
                )
                r = 0
                if "Datetime" in self.merged_data.columns:
                    for v in self.merged_data["Datetime"]:
                        self.merged_data.loc[r, "Datetime"] = v[:19]
                        r += 1
                self.new_data_csv = self.merged_data.drop_duplicates()
                self.new_data_csv.to_csv(
                    f'{self.path}\\{ticker["Ticker"]}', index=False
                )

            #  Creating excel file
            if self.checkbox == 1:
                self.excel_path = f'{self.dest_folder}\\{ticker["Ticker"]}\\{ticker["Interval"]}\\EXCEL CSV'
                if not os.path.exists(self.excel_path):
                    os.makedirs(self.excel_path)
                self.new_data_csv.to_excel(
                    f'{self.excel_path}\\{ticker["Ticker"]}.xlsx',
                    index=False,
                    header=True,
                )

