# Compare Appsilon model outputs
# Created November 5, 2024

library(tidyverse)

# **Read the outputs**

# Prosome segmentation of LOKI images
loki.prosome <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/loki_prosome/prediction_results.csv") %>% 
  rename(prosome_pixels_annotated = lipid_pixels_annotated) %>% 
  rename(prosome_pixels_predicted = lipid_pixels_predicted)


# The lipid segmentation using the original Appsilon model
loki.lipid.orig <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/loki_orig_model/prediction_results.csv")


# The lipid segmentation using the retrained model on the cropped prosomes
loki.lipid.crop <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/loki_prosome_cropped/prediction_results.csv")

# The lipid segmentation of the downscaled Loki images to /4
loki.lipid.down4 <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/loki_downscale_4/prediction_results.csv") %>% 
  mutate(lipid_mass_annotated = lipid_mass_annotated * 4 * 4,
         lipid_mass_predicted = lipid_mass_predicted * 4 * 4) # reverse the mass conversion for each pixel



# The UVP6 test runs using the downscalled LOKI
uvp6.test <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/uvp6_test/prediction_results.csv")

# Add metadata table for LOKI images indicating which ones were used for training/test
# ! The is_valid variable determines if the image was used in the training (FALSE)
meta.lipidsPaper <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/metadata_full.csv") %>% 
  mutate(data_use = if_else(is_valid == "True", "test", "train"))


# The analysis of the Maps et al. 2023 paper
ggplot(meta.lipidsPaper, aes(x = copepod_area_pixels,
                      y = IoU, color = data_use)) +
  geom_point(alpha = 0.2) +
  geom_hline(yintercept = .80, linetype = "dashed", color = "orange") +
  geom_hline(yintercept = .90, linetype = "longdash", color = "orange") +
  geom_smooth() +
  ggtitle(paste0("Maps et al. 2023 results, IoU = ", 
                 sprintf("%.1f",mean(meta.lipidsPaper$IoU))))


ggplot(meta.lipidsPaper, aes(x = (copepod_mass_annotated - copepod_mass_pred),
                             fill = data_use)) +
  geom_histogram() +
  xlab("difference in mass (mg)") +
  ggtitle(paste0("Maps et al. 2023 results, RMSE = ", 
                 sprintf("%.3f", sqrt(mean(meta.lipidsPaper$copepod_mass_annotated -
                                             meta.lipidsPaper$copepod_mass_pred)^2)),
                 " mg"))


# Average IoUs
mean(loki.prosome$percent_overlap)
mean(loki.lipid.orig$percent_overlap)
mean(loki.lipid.crop$percent_overlap)
mean(loki.lipid.down4$percent_overlap)
mean(uvp6.test$percent_overlap)

median(loki.prosome$percent_overlap)
median(loki.lipid.orig$percent_overlap)
median(loki.lipid.crop$percent_overlap)
median(loki.lipid.down4$percent_overlap)
median(uvp6.test$percent_overlap)


# IoU vs segmentation area in pixels
ggplot(loki.prosome, aes(x = lipid_pixels_annotated,
                         y = percent_overlap)) +
  geom_point(alpha = 0.2) +
  geom_hline(yintercept = 80, linetype = "dashed", color = "orange") +
  geom_hline(yintercept = 90, linetype = "longdash", color = "orange") +
  geom_smooth() +
  ggtitle(paste0("Prosome segmentation, IoU = ", 
                 sprintf("%.1f",mean(loki.prosome$percent_overlap))))

ggplot(loki.lipid.orig, aes(x = lipid_pixels_annotated,
                         y = percent_overlap)) +
  geom_point(alpha = 0.2) +
  geom_hline(yintercept = 80, linetype = "dashed", color = "orange") +
  geom_hline(yintercept = 90, linetype = "longdash", color = "orange") +
  geom_smooth() +
  ggtitle(paste0("Lipid segmentation with original model, IoU = ", 
          sprintf("%.1f",mean(loki.lipid.orig$percent_overlap))))

ggplot(loki.lipid.crop, aes(x = lipid_pixels_annotated,
                            y = percent_overlap)) +
  geom_point(alpha = 0.2) +
  geom_hline(yintercept = 80, linetype = "dashed", color = "orange") +
  geom_hline(yintercept = 90, linetype = "longdash", color = "orange") +
  geom_smooth() +
  ggtitle(paste0("Lipid segmentation with retrained cropped prosome model, IoU = ", 
                 sprintf("%.1f",mean(loki.lipid.crop$percent_overlap))))


ggplot(loki.lipid.down4, aes(x = lipid_pixels_annotated,
                            y = percent_overlap)) +
  geom_point(alpha = 0.2) +
  geom_hline(yintercept = 80, linetype = "dashed", color = "orange") +
  geom_hline(yintercept = 90, linetype = "longdash", color = "orange") +
  geom_smooth() +
  ggtitle(paste0("Lipid segmentation of downscaled /4 LOKI, IoU = ", 
                 sprintf("%.1f",mean(loki.lipid.crop$percent_overlap))))


ggplot(uvp6.test, aes(x = lipid_pixels_annotated,
                            y = percent_overlap)) +
  geom_point(alpha = 0.2) +
  geom_hline(yintercept = 80, linetype = "dashed", color = "orange") +
  geom_hline(yintercept = 90, linetype = "longdash", color = "orange") +
  geom_smooth() +
  ggtitle(paste0("Lipid segmentation of UVP6 using LOKI downscale, IoU = ", 
                 sprintf("%.1f",mean(uvp6.test$percent_overlap))))





# Calculate the spread of the error of segmentation estimates, and the RMSE
ggplot(loki.prosome, aes(x = (prosome_mass_annotated - prosome_mass_predicted))) +
  geom_histogram() +
  xlab("difference in mass (mg)") +
  ggtitle(paste0("Prosome segmentation, RMSE = ", 
                 sprintf("%.3f", sqrt(mean(loki.prosome$prosome_mass_annotated -
                                         loki.prosome$prosome_mass_predicted)^2)),
                 " mg"))

ggplot(loki.lipid.orig, aes(x = (lipid_mass_annotated - lipid_mass_predicted))) +
  geom_histogram() +
  xlab("difference in mass (mg)") +
  ggtitle(paste0("Lipid segmentation orig, RMSE = ", 
                 sprintf("%.3f", sqrt(mean(loki.lipid.orig$lipid_mass_annotated -
                                             loki.lipid.orig$lipid_mass_predicted)^2)),
                 " mg"))

ggplot(loki.lipid.crop, aes(x = (lipid_mass_annotated - lipid_mass_predicted))) +
  geom_histogram() +
  xlab("difference in mass (mg)") +
  ggtitle(paste0("Lipid segmentation crop, RMSE = ", 
                 sprintf("%.3f", sqrt(mean(loki.lipid.crop$lipid_mass_annotated -
                                             loki.lipid.crop$lipid_mass_predicted)^2)),
                 " mg"))

ggplot(loki.lipid.down4, aes(x = (lipid_mass_annotated - lipid_mass_predicted))) +
  geom_histogram() +
  xlab("difference in mass (mg)") +
  ggtitle(paste0("Lipid segmentation /4 downscale, RMSE = ", 
                 sprintf("%.3f", sqrt(mean(loki.lipid.down4$lipid_mass_annotated -
                                             loki.lipid.down4$lipid_mass_predicted)^2)),
                 " mg"))

ggplot(uvp6.test, aes(x = (lipid_mass_annotated - lipid_mass_predicted))) +
  geom_histogram() +
  xlab("difference in mass (mg)") +
  ggtitle(paste0("Lipid segmentation UVP6, RMSE = ", 
                 sprintf("%.3f", sqrt(mean(uvp6.test$lipid_mass_annotated -
                                             uvp6.test$lipid_mass_predicted)^2)),
                 " mg"))



# Prosome pixels vs lipid pixels
# Is there a relationship that could be used as an empirical function?
prosome.lipid <- loki.prosome %>% 
  select(-c(directory, percent_overlap, percent_of_annotated)) %>% 
  left_join(loki.lipid.crop,
            by = join_by(filename)) %>% 
  select(-c(directory, percent_overlap, percent_of_annotated)) 

ggplot(prosome.lipid, aes(x = prosome_pixels_annotated,
                          y = lipid_pixels_annotated)) +
  geom_point(alpha = 0.2) +
  geom_smooth()

# If based on predicted, could work... but the lipid prediction more typically predict zero or very low lipid mass
ggplot(prosome.lipid, aes(x = prosome_pixels_predicted,
                          y = lipid_pixels_predicted)) +
  geom_point(alpha = 0.2) +
  geom_smooth()

# Empirical model for estimating lipid area if only given the prosome area
# R2adj = 0.863
em.prosome.lipid <- lm(lipid_pixels_annotated ~ prosome_pixels_annotated,
                       data = prosome.lipid)
summary(em.prosome.lipid)
