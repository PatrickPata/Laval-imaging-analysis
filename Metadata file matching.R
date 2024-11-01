# Match the copepod prosome and lipid masks to update the metadata file
# Created October 31, 2024
#
#
# Load the metadata file used in the original Appsilon model.
lipidsPaper <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/metadata_full.csv")

# IoU vs lipid mask - This will show a nonlinear curve wherein lower IoU are instances when lipid mass is lowest. Therefore the model performs best for larger copepods with larger lipid contents.
plot(lipidsPaper$copepod_mass_annotated, lipidsPaper$IoU)
# plot(lipidsPaper$copepod_mass_pred, lipidsPaper$IoU)

# Load Cyril's table of file matching
cyrilCurated <- readxl::read_xlsx("C:/Users/patri/OneDrive - Université Laval/Laval_Postdoc/Laval-imaging-analysis/LOKI-segmentation/loki_segmentation_dataset_df_Cyril20241030.xlsx") %>% 
  filter(object_id != "ecotaxa table JPR-2023-061.tsv") %>% 
  # This is a duplicated file pointing to the same image file: 20130815 104419 867 000000 0996 0096.bmp
  filter(idx != 228)

# Filter the list of files to get only those with both lipid and prosome masks.
fileList <- cyrilCurated %>% 
  # The copepods with image files. Will match the list in the lipids paper.
  filter(filename_bmp_img %in% lipidsPaper$filename) %>% 
  # filter(!is.na(filename_bmp_img)) %>%  # This is supposed to produce the same result as the line above.
 
  # filter only images with both prosome and lipid masks
  filter(!is.na(filename_lipid_mask)) %>% 
  filter(!is.na(filename_prosome_mask)) %>% 
  
  # reduce columns
  select(idx, object_id, filename = filename_bmp_img,
         filename_prosome_mask, filename_lipid_mask) %>% 
  
  # Merge the metadata file with the list of prosome masks
  left_join(lipidsPaper)

# Export updated metadata file
write.csv(fileList,
          file = "C:/Users/patri/python_workspace/copepods-lipid-content/metadata_prosome_lipid.csv")
