clc
clear
close all
tic
%% Read Input Image and convert to CieLAB Space

[file,path] = uigetfile('mzunig2.png');
f = fullfile(path,file);
a = imread(f);
% a = imresize(a,0.5);
a_lab = rgb2lab(a);
%% Uncomment for the fire effect
% labTransformation = makecform('srgb2lab');
% a_lab = double(applycform(a,labTransformation));

%% Parameters

m = 15;
n = 5;     %threshold on no. of iterations
k = 100;
%% 
N = size(a,1)*size(a,2);

s = sqrt(N/k);

%% Gradient Image
G = zeros(size(a,1)-1,size(a,2)-1);
for i = 2:size(a,1)-1
    for j = 2:size(a,2)-1
        gx = (squeeze(a_lab(i+1,j,:))-squeeze(a_lab(i-1,j,:)));
        gy = (squeeze(a_lab(i,j+1,:))-squeeze(a_lab(i,j-1,:)));
        G(i,j) = gx(1)^2 + gx(2)^2 + gx(3)^2 + gy(1)^2 + gy(2)^2 + gy(3)^2;
    end
end
% figure;
% imagesc(G);

%% Initializing the Centers
s = ceil(s);
cx = s:s:size(a,1)-s;
cy = s:s:size(a,2)-s;
p=1;
for i = 1:size(cx,2)
    for j = 1:size(cy,2)
        loc(p,:) = [cx(i),cy(j)];
        p=p+1;
    end
end

for i = 1:size(loc,1)
    c(i,:) = [a_lab(loc(i,1),loc(i,2),1) a_lab(loc(i,1),loc(i,2),2) a_lab(loc(i,1),loc(i,2),3) loc(i,1) loc(i,2)];
end

%% SLIC Algorithm
win = 7;
n1 = floor(win/2);

lochange = -n1:n1;


for i = 1:size(loc,1)
    H = G(loc(i,1)-n1:loc(i,1)+n1,loc(i,2)-n1:loc(i,2)+n1);
    [a1,b1] = min(H);
    [a2,b2] = min(a1);
    loc(i,1) = loc(i,1) + lochange(b1(b2));
    loc(i,2) = loc(i,2) + lochange(b2);
    c(i,:) = [a_lab(loc(i,1),loc(i,2),1) a_lab(loc(i,1),loc(i,2),2) a_lab(loc(i,1),loc(i,2),3) loc(i,1) loc(i,2)];
end

iter = 0;
msg = 'Segmenting ...';
x = 0;
f = waitbar(x,msg);
while iter < n
   
   for i2 = 1:size(a,1)
       for j2 = 1:size(a,2)
           dis = [];
           for k2 = 1:size(loc,1)
               if sqrt((i2-loc(k2,1))^2 + (j2 - loc(k2,2))^2) < 2*s
                   d = sqrt((a_lab(i2,j2,1)-c(k2,1))^2 + (a_lab(i2,j2,2)-c(k2,2))^2 + (a_lab(i2,j2,3)-c(k2,3))^2) + m/s*sqrt((i2-c(k2,4))^2 + (j2-c(k2,5))^2);
                   dis = [dis;d k2];
               end
           end
           if isempty(dis)
           else
           [mind,I] = min(dis(:,1));
           o(i2,j2) = dis(I,2);
           end
       end
   end
   
   for i3 = 1:size(loc,1)
       [row,col] = find(o==i3);
       if isempty(row) && isempty(col)
       else
       rowmean = round(mean(row));
       colmean = round(mean(col));
       c(i3,:)=[a_lab(rowmean,colmean,1) a_lab(rowmean,colmean,2) a_lab(rowmean,colmean,3) rowmean colmean];
       end
   end
   
   iter = iter +1;
    x = iter/(n);
    waitbar(x,f)
%    %% Uncomment Following lines to see the image at every step
%    for i4 = 1:size(a,1)
%     for j4 = 1:size(a,2)
%         for k4 = 1:3
%         if o(i4,j4)~=0
%         out(i4,j4,k4) = c(o(i4,j4),k4);
%         end
%     end
%     end
% end
%    
% out1 = lab2rgb(out)*255;
% figure;
% imshow(uint8(out1));
% 
% outvid(:,:,:,iter) = uint8(out1);
end
close(f)
%%
for i4 = 1:size(a,1)
    for j4 = 1:size(a,2)
        for k4 = 1:3
        if o(i4,j4)~=0
        out(i4,j4,k4) = c(o(i4,j4),k4);
        end
        end
    end
end
% 
% cform = makecform('lab2srgb');
% out1 = applycform(out,cform);    
out1 = lab2rgb(out)*255;

%Separación  
[R,G,B] = imsplit(out1);
imshow(uint8(out1));
figure;
imshow(uint8(R));
figure;
imshow(uint8(G));
figure;
imshow(uint8(B));
%% Edges on the image
d = double(edge((rgb2gray(uint8(out1))),'canny'));
d(find(d==1)) = 255;
d(find(d==0)) = 1;
d(find(d==255)) = 0;
f1 = out1.*d;
%figure;
%imshow(uint8(f1))
%%
toc