import os
import zipfile
import arcpy
from arcpy.sa import *

# ✅ Enable Spatial Analyst
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

# 📁 Input ZIP folder and unzip destination
zip_folder = r"C:\DEMO"
unzip_root = r"C:\DEMO2"

# 📁 Output folders
final_output_folder = r"C:\DEMO\clipped_composite"
ndvi_output_folder = r"C:\DEMO\NDVI_Results"
ndvi_visual_folder = r"C:\DEMO\NDVI_Visuals"

os.makedirs(final_output_folder, exist_ok=True)
os.makedirs(ndvi_output_folder, exist_ok=True)
os.makedirs(ndvi_visual_folder, exist_ok=True)

# 🎯 Shapefile for clipping
mask_shapefile = r"C:\District_Boundary_Sonipat.shp"

# 🛰️ Required 20m bands
required_bands = ["B02", "B03", "B04", "B08"]

composite_clipped_list = []
ndvi_clipped_list = []

# 🔁 Loop through each ZIP file
for zip_file in os.listdir(zip_folder):
    if zip_file.endswith(".zip"):
        zip_path = os.path.join(zip_folder, zip_file)
        zip_name = os.path.splitext(zip_file)[0]
        unzip_path = os.path.join(unzip_root, zip_name)
        os.makedirs(unzip_path, exist_ok=True)

        # ✅ Unzip
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        print(f"✅ Unzipped: {zip_file}")

        # 🔍 Locate R20m folder
        r20m_folder = ""
        for root, dirs, files in os.walk(unzip_path):
            if os.path.basename(root) == "R20m":
                r20m_folder = root
                break

        if not r20m_folder:
            print(f"❌ R20m folder not found in {zip_file}")
            continue

        band_files = []
        band_dict = {}
        for band_id in required_bands:
            matched = False
            for file in os.listdir(r20m_folder):
                if f"{band_id}_20m" in file and file.endswith(".jp2"):
                    band_path = os.path.join(r20m_folder, file)
                    band_files.append(band_path)
                    band_dict[band_id] = band_path
                    matched = True
                    break
            if not matched:
                print(f"❌ Band {band_id}_20m not found in {zip_file}")

        if len(band_files) != len(required_bands):
            print(f"⚠️ Skipping {zip_file}: Not all required bands found")
            continue

        # 🌈 Composite
        composite_path = os.path.join(unzip_path, f"Composite_{zip_name}.tif")
        arcpy.management.CompositeBands(band_files, composite_path)
        print(f"🌈 Composite created: {composite_path}")

        # ✂️ Clip Composite with Extract by Mask
        arcpy.env.snapRaster = composite_path
        clipped_output = os.path.join(final_output_folder, f"Clipped_{zip_name}.tif")
        clipped_raster = ExtractByMask(composite_path, mask_shapefile)
        clipped_raster.save(clipped_output)
        print(f"✂️ Clipped composite saved: {clipped_output}")
        composite_clipped_list.append(clipped_output)

        # 🌿 NDVI Calculation
        try:
            red = Raster(band_dict["B04"])
            nir = Raster(band_dict["B08"])
            print("📌 NDVI bands loaded successfully from unzipped folder")

            ndvi = (nir - red) / (nir + red)

            # ✂️ Clip NDVI
            ndvi_clipped = ExtractByMask(ndvi, mask_shapefile)
            ndvi_output_path = os.path.join(ndvi_output_folder, f"NDVI_{zip_name}.tif")
            ndvi_clipped.save(ndvi_output_path)
            print(f"🌿 Clipped NDVI saved: {ndvi_output_path}")
            ndvi_clipped_list.append(ndvi_output_path)

            # 🖼️ Export NDVI JPEG for Visualization
            ndvi_jpeg_path = os.path.join(ndvi_visual_folder, f"NDVI_{zip_name}.jpg")
            arcpy.management.CopyRaster(
                ndvi_output_path,
                ndvi_jpeg_path,
                pixel_type="32_BIT_FLOAT",
                format="JPEG",
                nodata_value="0"
            )
            print(f"🖼️ NDVI JPEG exported: {ndvi_jpeg_path}")

        except Exception as e:
            print(f"❌ NDVI failed for {zip_file}: {e}")

# 🧱 Mosaic Clipped Composite Rasters
if composite_clipped_list:
    mosaic_composite_output = os.path.join(final_output_folder, "Mosaic_Composite.tif")
    arcpy.management.MosaicToNewRaster(composite_clipped_list, final_output_folder, "Mosaic_Composite.tif",
                                       pixel_type="32_BIT_FLOAT", number_of_bands=4)
    print(f"🧱 Mosaic composite created: {mosaic_composite_output}")

# 🧱 Mosaic Clipped NDVI Rasters
if ndvi_clipped_list:
    mosaic_ndvi_output = os.path.join(ndvi_output_folder, "Mosaic_NDVI.tif")
    arcpy.management.MosaicToNewRaster(ndvi_clipped_list, ndvi_output_folder, "Mosaic_NDVI.tif",
                                       pixel_type="32_BIT_FLOAT", number_of_bands=1)
    print(f"🧱 Mosaic NDVI created: {mosaic_ndvi_output}")

print("🎉 All Sentinel-2 ZIPs processed with composite, clipping, NDVI, JPEG export, and mosaicking!")
