#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import geopandas as gpd
import pandas as pd
import numpy as np
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import customtkinter as ctk
import matplotlib.pyplot as plt
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class Minus9999GISCleaner(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("-9999 GIS Data Cleaner")
        self.geometry("720x540")
        self.file_path = None
        self.cleaned_df = None
        self.original_df = None
        self.num_cols = []
        self.filename_prefix = ""

        # === UI Layout ===
        ctk.CTkLabel(self, text="-9999 GIS Data Cleaner", font=("Arial", 22)).pack(pady=10)

        ctk.CTkButton(self, text="📂 Browse File", command=self.browse_file).pack(pady=5)

        self.summary_label = ctk.CTkLabel(self, text="Summary will appear here", wraplength=650, justify="left")
        self.summary_label.pack(pady=10)

        self.format_select = ctk.CTkComboBox(self, values=[".csv", ".xlsx", ".shp"])
        self.format_select.set(".csv")
        ctk.CTkLabel(self, text="Choose Output Format:").pack()
        self.format_select.pack(pady=5)

        ctk.CTkButton(self, text="🧼 Clean Data", command=self.clean_data).pack(pady=10)
        ctk.CTkButton(self, text="📊 Show Visualizations", command=self.visualize_all).pack(pady=5)
        ctk.CTkButton(self, text="💾 Export Cleaned File", command=self.export_file).pack(pady=20)
        ctk.CTkButton(self, text="ℹ️ About", command=self.show_about).pack(pady=5)

    def browse_file(self):
        path = fd.askopenfilename(filetypes=[("Supported", "*.shp *.csv *.xlsx")])
        if path:
            self.file_path = path
            self.filename_prefix = os.path.splitext(os.path.basename(path))[0]
            ext = os.path.splitext(path)[-1].lower()
            try:
                if ext == ".csv":
                    df = pd.read_csv(path)
                elif ext in [".xlsx", ".xls"]:
                    df = pd.read_excel(path)
                elif ext == ".shp":
                    df = gpd.read_file(path)
                else:
                    mb.showerror("Unsupported", "Only .shp, .csv, .xlsx files are supported.")
                    return

                if isinstance(df, gpd.GeoDataFrame):
                    self.display_shapefile_info(df)
                else:
                    self.summary_label.configure(text=f"✅ File loaded. Ready to clean.")

                self.original_df = df.copy()

            except Exception as e:
                mb.showerror("Load Error", str(e))

    def display_shapefile_info(self, gdf):
        self.num_cols = gdf.select_dtypes(include=["number"]).columns.tolist()

        gdf_info = f"✅ Shapefile Loaded\n"
        gdf_info += f"📌 Total features: {len(gdf)}\n\n"
        gdf_info += f"🔎 First 5 records:\n{gdf.head(5)}\n\n"

        missing_9999 = (gdf[self.num_cols] == -9999).sum()
        gdf_info += f"⚠️ -9999 Counts per Column:\n{missing_9999.to_string()}"

        self.summary_label.configure(text=gdf_info)

    def clean_data(self):
        if not self.file_path:
            mb.showwarning("Missing File", "Please select a file first.")
            return

        ext = os.path.splitext(self.file_path)[-1].lower()
        try:
            if ext == ".csv":
                df = pd.read_csv(self.file_path)
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(self.file_path)
            elif ext == ".shp":
                df = gpd.read_file(self.file_path)
            else:
                mb.showerror("Unsupported", "Unsupported file type.")
                return

            self.num_cols = df.select_dtypes(include=["number"]).columns.tolist()

            # Replace -9999 with NaN
            df[self.num_cols] = df[self.num_cols].replace(-9999, np.nan)

            # Add missing flag before clean
            if isinstance(df, gpd.GeoDataFrame):
                df["any_null"] = df[self.num_cols].isnull().any(axis=1)

            self.original_df = df.copy()

            # Forward fill
            df = df.sort_index()
            df[self.num_cols] = df[self.num_cols].ffill()

            self.cleaned_df = df

            missing_after = df[self.num_cols].isnull().sum()
            fixed_summary = f"✅ Cleaned! Missing values AFTER cleaning:\n\n{missing_after.to_string()}"
            self.summary_label.configure(text=fixed_summary)

        except Exception as e:
            mb.showerror("Cleaning Error", str(e))

    def visualize_all(self):
        if not isinstance(self.cleaned_df, gpd.GeoDataFrame):
            mb.showinfo("Note", "Visualization only available for shapefiles.")
            return

        try:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_dir = os.path.dirname(self.file_path)

            # Before Cleaning
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            self.original_df.plot(ax=ax1, column="any_null", categorical=True, legend=True, cmap="coolwarm", markersize=10)
            ax1.set_title("🔴 Missing Data (-9999) Before Cleaning")
            ax1.axis("off")
            plt.tight_layout()
            fig1.savefig(f"{out_dir}/{self.filename_prefix}_missing_before_{now}.png")
            plt.show()

            # After Cleaning
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            self.cleaned_df.plot(ax=ax2, color="green", markersize=10)
            ax2.set_title("✅ After Forward Fill")
            ax2.axis("off")
            plt.tight_layout()
            fig2.savefig(f"{out_dir}/{self.filename_prefix}_cleaned_after_{now}.png")
            plt.show()

            # Final Missing Check
            self.cleaned_df["has_missing"] = self.cleaned_df[self.num_cols].isnull().any(axis=1)

            fig3, ax3 = plt.subplots(figsize=(10, 6))
            self.cleaned_df.plot(ax=ax3, color="lightgrey", markersize=5)
            if self.cleaned_df["has_missing"].any():
                self.cleaned_df[self.cleaned_df["has_missing"]].plot(ax=ax3, color="red", markersize=5, label="Still Missing")
                plt.legend()
            ax3.set_title("📍 Final Data Check")
            ax3.axis("off")
            plt.tight_layout()
            fig3.savefig(f"{out_dir}/{self.filename_prefix}_post_fill_check_{now}.png")
            plt.show()

            mb.showinfo("Visualization Saved",
                        "All maps saved as PNG in the same folder as your input file.")

        except Exception as e:
            mb.showerror("Visualization Error", str(e))

    def export_file(self):
        if self.cleaned_df is None:
            mb.showwarning("No Data", "Please clean your data first.")
            return

        ext = self.format_select.get()
        save_path = fd.asksaveasfilename(defaultextension=ext,
                                         filetypes=[("CSV", "*.csv"), ("Excel", "*.xlsx"), ("Shapefile", "*.shp")])
        if not save_path:
            return

        try:
            if ext == ".csv":
                self.cleaned_df.to_csv(save_path, index=False)
            elif ext in [".xlsx", ".xls"]:
                self.cleaned_df.to_excel(save_path, index=False)
            elif ext == ".shp":
                if isinstance(self.cleaned_df, gpd.GeoDataFrame):
                    self.cleaned_df.to_file(save_path)
                else:
                    mb.showerror("Export Error", "Not a shapefile input.")
                    return
            mb.showinfo("Exported", f"File saved to:\n{save_path}")
        except Exception as e:
            mb.showerror("Export Error", str(e))

    def show_about(self):
        mb.showinfo("About", (
            "-9999 GIS Data Cleaner\n"
            "Version 1.0 (2025)\n"
            "Developed by [SAYANTAN MANDAL]\n"
            "Cleans and visualizes GIS files with -9999 errors.\n"
            "Supports SHP, CSV, XLSX formats.\n"
            "All rights reserved © 2025"
        ))


if __name__ == "__main__":
    app = Minus9999GISCleaner()
    app.mainloop()


# In[ ]:




