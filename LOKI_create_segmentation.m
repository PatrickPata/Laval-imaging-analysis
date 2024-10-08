% Creating segmentation files
% Created by P. Pata
% Created on Oct 3, 2024

seg_list = readtable('C:/Laval_Postdoc/Laval-imaging-analysis/LOKI images/LOKI images/data and readme/copepod_segmentation.csv');

% % Filter the seg_list to only the files in pred_list (not sure if this is
% a good idea so don't do it for now).
% pred_list = readtable('C:/Laval_Postdoc/Laval-imaging-analysis/LOKI images/LOKI images/data and readme/prediction_results.csv');
% [C,ia,ib]  = intersect(pred_list.filename, pred_list.filename);
% AA = seg_list(ia,:);


% Get the sizes of the individual files
matrix_sizes = split(seg_list.shape,'(');
matrix_sizes = split(matrix_sizes(:,2),')');
matrix_sizes = split(matrix_sizes(:,1),',');
matrix_sizes = str2double(matrix_sizes);


for i = 1:height(seg_list)

    % Identify file name
    fname = seg_list.filename(i);
    fname_out = strcat('LOKI images/LOKI images/copepod_segmentations/',fname{1});

    % Load the polygon
    poly = seg_list.segmentation{i};
    poly = split(poly, '],');
    poly = split(poly, ',');
    poly = erase(poly, '[');
    poly = erase(poly, ']');
    poly = str2double(poly);

    % Create the mask using matrix limits
    mask = poly2mask(poly(:,1), poly(:,2), matrix_sizes(i,1), matrix_sizes(i,2));

    % Convert logical to uint8? or double?
    mask = im2uint8(mask)/255;

    % figure; pcolor(flipud(mask2)); shading flat

    % Output the bmp file
    imwrite(mask, fname_out)

end