% Testing LOKI image downscaling
% Created by P. Pata
% Created on Oct 3, 2024

% A. Set parameters
datafolimg = 'C:/Laval_Postdoc/Laval-imaging-analysis/example_inputs/';
datafolseg = 'C:/Laval_Postdoc/Laval-imaging-analysis/example_segmentations/';
resFactor = 4; % Rescale image n-times lower
resFactorFrac = 1/resFactor;
outfolimg = 'C:/Laval_Postdoc/Laval-imaging-analysis/example_lowres_inputs/';
outfolseg = 'C:/Laval_Postdoc/Laval-imaging-analysis/example_lowres_segmentations/';

% The diagnostics table to output.
imgInfo = {};

% B. Set up loop over all images in folder
dinfo = dir(datafolimg);
full_filenames = fullfile({dinfo.name});
full_filenames = full_filenames(3:length(full_filenames));
% The list of filenames of images and segmentations should match so only
% load the list for images.

for ii = 1:length(full_filenames)

    % 1. Load some LOKI images
    I = imread(strcat(datafolimg,full_filenames{ii}));
    Seg = imread(strcat(datafolseg,full_filenames{ii}));

    % Need to crop the image to be a multiple of the resFactor to calculate
    % the error after rescaling.
    
    dimX = size(I,2);
    dimY = size(I,1);
    xlim = floor(dimX/resFactor)*resFactor;
    ylim = floor(dimY/resFactor)*resFactor;
    cropX = dimX - xlim;
    cropY = dimY - ylim;
    I = imcrop(I, [0 0 xlim ylim]);
    Seg = imcrop(Seg, [0 0 xlim ylim]);


    % figure; imshow(I)
    % figure; pcolor(flipud(Seg)); shading flat

    % 2. Reduce by factor of 4. Uses bicubic interpolation by default.
    Ilow = imresize(I, resFactorFrac);
    % figure; imshow(Ilow)

    Seglow = imresize(Seg, resFactorFrac);
    % figure; pcolor(flipud(Seglow)); shading flat

    % 3. Scale the value back up to get information lost especially for lipid
    % area.
    Ihigh = imresize(Ilow, resFactor);
    Seghigh = imresize(Seglow, resFactor);

    % figure; imshow(Ihigh)
    % figure; pcolor(flipud(Seghigh)); shading flat

    lipidErr = Seg - Seghigh;
    % figure; pcolor(flipud(lipidErr)); shading flat

    lipidArea = sum(sum(Seg));
    lipidErrSum = sum(sum(abs(lipidErr)));
    lipidErrPercLipid = (lipidErrSum / lipidArea) * 100;
    lipidErrPercGrid = (lipidErrSum / prod(size(Seg))) * 100;

    disp(strcat('Image #', num2str(ii), ' rescale error:  ', ...
        num2str(lipidErrPercLipid,'%.1f'), '%'))

    imgInfo = cat(1, imgInfo, {full_filenames{ii}, resFactor, ...
        dimX, dimY, cropX, cropY, ...
        lipidArea, lipidErrPercLipid, lipidErrPercGrid});

    % 4. Output the low res image and note error in file name
    imwrite(Ilow, ...
        strcat(outfolimg, 'rf_', num2str(resFactor), ...
        '_err_', num2str(lipidErrPercLipid,'%.1f'), ...
        '_',full_filenames{ii}))
    imwrite(Seghigh, ...
        strcat(outfolseg, 'rf_', num2str(resFactor), ...
        '_err_', num2str(lipidErrPercLipid,'%.1f'), ...
        '_',full_filenames{ii}))
end

% C. Output the diagnostic file.
imgInfo = array2table(imgInfo);
imgInfo.Properties.VariableNames(1:9) = {'filename','resize_factor', ...
    'dimX','dimY','xcrop','ycrop',...
    'n_lipid_pixels', 'rescale_error', 'error_per_grid'};
writetable(imgInfo,strcat( strcat(outfolseg,'resize_diagnostics.csv')))