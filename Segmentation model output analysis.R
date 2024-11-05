# Compare Appsilon model outputs
# Created November 5, 2024

library(tidyverse)

# **Read the outputs**

# Prosome segmentation of LOKI images
loki.prosome <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/loki_prosome/prediction_results.csv")


# The lipid segmentation using the original Appsilon model
loki.lipid.orig <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/loki_orig_model/prediction_results.csv")


# The lipid segmentation using the retrained model on the cropped prosomes
loki.lipid.crop <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/loki_prosome_cropped/prediction_results.csv")

# The UVP6 test runs using the downscalled LOKI
uvp6.test <- read.csv("C:/Users/patri/python_workspace/copepods-lipid-content/prediction_outputs/uvp6_test/prediction_results.csv")


# Average IoUs
mean(loki.prosome$percent_overlap)
mean(loki.lipid.orig$percent_overlap)
mean(loki.lipid.crop$percent_overlap)
mean(uvp6.test$percent_overlap)

median(loki.prosome$percent_overlap)
median(loki.lipid.orig$percent_overlap)
median(loki.lipid.crop$percent_overlap)
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

ggplot(uvp6.test, aes(x = lipid_pixels_annotated,
                            y = percent_overlap)) +
  geom_point(alpha = 0.2) +
  geom_hline(yintercept = 80, linetype = "dashed", color = "orange") +
  geom_hline(yintercept = 90, linetype = "longdash", color = "orange") +
  geom_smooth() +
  ggtitle(paste0("Lipid segmentation of UVP6 using LOKI downscale, IoU = ", 
                 sprintf("%.1f",mean(uvp6.test$percent_overlap))))


