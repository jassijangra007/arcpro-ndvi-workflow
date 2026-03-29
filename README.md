# arcpro-ndvi-workflow
Automated Sentinel-2 processing workflow in ArcGIS Pro using ArcPy: band compositing, clipping, NDVI calculation, visualization, and mosaicking.


# 🌍 ArcGIS Pro Sentinel-2 NDVI Automation

This repository contains a Python (ArcPy) workflow for processing Sentinel-2 satellite imagery in **ArcGIS Pro**.

It automates:

* Unzipping Sentinel-2 data
* Band compositing (B02, B03, B04, B08)
* Raster clipping using shapefile
* NDVI calculation
* NDVI visualization export (JPEG)
* Mosaic creation (Composite + NDVI)

---

## 🚀 Features

✅ Fully automated Sentinel-2 ZIP processing
✅ Works inside ArcGIS Pro (ArcPy)
✅ NDVI calculation using Red & NIR bands
✅ Clip using district/area boundary
✅ Export NDVI as GeoTIFF + JPEG
✅ Mosaic multiple rasters

---

## 📂 Folder Structure

```
C:\Jassi\DEMO
│
├── ZIP files (Sentinel-2)
├── clipped_composite/
├── NDVI_Results/
├── NDVI_Visuals/
```

---

## 📌 Requirements

* ArcGIS Pro (with Spatial Analyst License)
* Python (comes with ArcGIS Pro)
* Sentinel-2 Level-2A data (.zip)
* Shapefile for clipping

---

## ⚙️ How It Works

1. Extracts all ZIP files
2. Finds `R20m` folder
3. Selects required bands:

   * B02 (Blue)
   * B03 (Green)
   * B04 (Red)
   * B08 (NIR)
4. Creates composite raster
5. Clips raster using shapefile
6. Computes NDVI:

   ```
   NDVI = (NIR - Red) / (NIR + Red)
   ```
7. Exports:

   * NDVI GeoTIFF
   * NDVI JPEG (visual)
8. Creates mosaics

---

## ▶️ Usage

1. Open **ArcGIS Pro Python environment**
2. Update paths in script:

   * ZIP folder
   * Output folders
   * Shapefile path
3. Run script

---

## 📊 Output

* Clipped Composite Images
* NDVI GeoTIFFs
* NDVI JPEG Visualizations
* Mosaic Composite
* Mosaic NDVI

---

## ⚠️ Important Notes

* Requires **Spatial Analyst Extension**
* Ensure correct band resolution (20m)
* Works best with Sentinel-2 L2A data
* Update file paths before running

---

## 👨‍💻 Author

Developed by Jassi for GIS & Remote Sensing workflows using ArcGIS Pro.

