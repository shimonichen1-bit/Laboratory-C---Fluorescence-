%settings:
img_path = 'C:\Users\ASUS\Desktop\fluorescence\b\e-4.jpg'; 
save_folder = 'C:\Users\ASUS\Desktop\fluorescence\b\graphs and data from matlab';

%original:
A = imread(img_path);
[~, name_only, ~] = fileparts(img_path);
A1 = im2double(A);

figure("Name", "image")
imagesc(A1(:,:,1))
title(['Click START and END of the beam for ', name_only]);

%choosing two points:
[x_clicks, y_clicks] = ginput(2); 
Av = improfile(A1(:,:,1), x_clicks, y_clicks, 3018); 
Av = Av'; %Transpose to keep original horizontal format

%graphing:
figure("Name", "graph")
x = linspace(0,10,length(Av));
plot(x, Av)

figure("Name", "Log Graph")
Avl = log(Av + 1e-6); % log of your extracted profile
plot(x, Avl)
xlabel('x [cm]')
ylabel('Power [AU]')
grid minor

%save cvs:
output_table = table(x', Av', 'VariableNames', {'Distance_cm', 'Intensity'});
full_save_path = fullfile(save_folder, [name_only, '_results.csv']);
writetable(output_table, full_save_path);

%sequence:
figure("Name", "image 2")
imagesc(A1(:,:,1)); imagesc(A1(:,:,2)); imagesc(A1(:,:,3));
imagesc(A1(:,:,1)); imagesc(A1(:,:,1)); imagesc(A1(:,:,2));
imagesc(A1(:,:,3)); imagesc(A1(:,:,1));

fprintf('Successfully saved: %s_results.csv\n', name_only);