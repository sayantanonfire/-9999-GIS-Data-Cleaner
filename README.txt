minus9999_GIS_Data_Cleaner
========================

🧼 This desktop tool is designed to help GIS professionals and researchers clean spatial datasets by identifying and correcting -9999 values, which typically represent missing or error data in geospatial layers.

Developed by:
Mr. Sayantan Mandal (PhD Research Scholar, Department of Geography, Delhi School of Economics, University of Delhi)
📧 sayantaninfire@gmail.com

----------------------------------------
📂 Supported File Formats:
✔️ Shapefiles (.shp)
✔️ Excel spreadsheets (.xlsx, .xls)
✔️ CSV tables (.csv)

----------------------------------------
🧠 Key Features:
- Automatically detects all -9999 values in numeric columns
- Replaces them with standard missing values (`NaN`)
- Performs forward-fill cleaning (i.e., fills missing data with the value directly above)
- Shows visual maps of missing vs. cleaned data (for shapefiles only)
- Saves visualizations as .PNG images in the same folder
- Allows export to your chosen format (.shp, .csv, .xlsx)

----------------------------------------
⚠️ Important Note about Forward-Fill:
Forward-fill means that missing values are filled using the value from the **row above**.

➡️ Therefore, please ensure that the **first data row** (i.e., the row immediately after the header) **is fully populated**, especially in GIS files.

If the first row is missing values, forward-fill cannot work properly and those values will remain `NaN`.

This tool is optimized for GIS table structures (attribute tables) where rows are spatially ordered and typically consistent.

----------------------------------------
🧭 How to Use:
1. Double-click the EXE file: `minus9999_GIS_Data_Cleaner.exe`
2. Upload your data file (.shp, .csv, .xlsx)
3. Review the top records and missing value summary
4. Click “Clean Data” to apply forward-fill
5. Click “Show Visualizations” (shapefile only)
6. Export your cleaned data using “Export File”

----------------------------------------
📸 Visualization:
- If your input is a `.shp`, you will get:
   - Map before cleaning (shows -9999 errors)
   - Map after forward-fill
   - Final check for any remaining missing values

These maps are saved automatically in PNG format alongside your input file (in the location of your input file in .png format).

----------------------------------------
🛠️ Disclaimer:
This tool is provided "as-is" for research and educational purposes. You are free to use, cite, and share it — but please credit the developer.

For bug reports, feature requests, or collaboration inquiries:
📨 Email: sayantaninfire@gmail.com

Thank you for using minus9999_GIS_Data_Cleaner!

