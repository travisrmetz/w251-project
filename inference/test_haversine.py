#test_haversine.py
#import haversine as hs 

from geopy.distance import geodesic


actual_lat=34.95968170768319
actual_long=-65.96097974743151
y_hat_lat=[36]
y_hat_long=[-70]

#loss_nm=hs.haversine_loss([actual_lat,actual_long],[y_hat_lat[0],y_hat_long[0]])
point1=(y_hat_lat[0],y_hat_long[0])
point2=(actual_lat,actual_long)
 
loss_nm=geodesic(point1,point2).nautical

print('Estimated latitude, longitude:',y_hat_lat[0],',',y_hat_long[0])
print('Actual latitude, longitude:',actual_lat,',',actual_long)
print('Error in nautical miles:',loss_nm)