% --- 1. SETTINGS (Change the number here for each run) ---
img_path = 'C:\Users\ASUS\Desktop\fluorescence\b\e-4.jpg'; 
save_folder = 'C:\Users\ASUS\Desktop\fluorescence\b\graphs and data from matlab';

% --- 2. YOUR ORIGINAL IMAGE SETUP ---
A = imread(img_path);
[~, name_only, ~] = fileparts(img_path);
A1 = im2double(A);

figure("Name", "image")
imagesc(A1(:,:,1))
title(['Click START and END of the beam for ', name_only]);

% --- 3. ADDED: CHOOSE THE TWO POINTS ---
[x_clicks, y_clicks] = ginput(2); 
% Extract profile (replaces the fixed 1908 row)
Av = improfile(A1(:,:,1), x_clicks, y_clicks, 3018); 
Av = Av'; % Transpose to keep your original horizontal format

% --- 4. YOUR ORIGINAL GRAPHING ---
figure("Name", "graph")
x = linspace(0,10,length(Av));
plot(x, Av)

figure("Name", "Log Graph")
Avl = log(Av + 1e-6); % log of your extracted profile
plot(x, Avl)
xlabel('x [cm]')
ylabel('Power [AU]')
grid minor

% --- 5. ADDED: SAVING THE CSV ---
output_table = table(x', Av', 'VariableNames', {'Distance_cm', 'Intensity'});
full_save_path = fullfile(save_folder, [name_only, '_results.csv']);
writetable(output_table, full_save_path);

% --- 6. YOUR ORIGINAL IMAGE SEQUENCE ---
figure("Name", "image 2")
imagesc(A1(:,:,1)); imagesc(A1(:,:,2)); imagesc(A1(:,:,3));
imagesc(A1(:,:,1)); imagesc(A1(:,:,1)); imagesc(A1(:,:,2));
imagesc(A1(:,:,3)); imagesc(A1(:,:,1));

fprintf('Successfully saved: %s_results.csv\n', name_only);