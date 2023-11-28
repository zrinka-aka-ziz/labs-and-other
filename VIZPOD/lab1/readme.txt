sadržaj zipa:
LAB1 - direktorij u kojemu se nalazi rješenje labosa i pripadne datoteke, stranica se pokreće s 'Go Live' na index.html
extras - direktorij s dodatnim datotekama korištenim pri izradi labosa, u njemu:
VIZPOD_LAB1_prep - Jupyter bilježnica korištena na Colabu za čišćenje i PCA analizu originalnog dataseta
spotify_songs - originalni dataset, preuzet s https://www.kaggle.com/datasets/joebeachcapital/30000-spotify-songs/
filtered_data - dataset s pjesmama odabranog izvođača (The Weeknd) i nekim manjim pretvorbama metrika, izborom značajki i sl.
data_no_color - dataset u formatu prikladnim za labos, bez stupca za boju heatmapa
data_color - kao prethodni, ali sadrži stupac color koji je samo kopija stupca value
data_color_final - konačni dataset s ispravnim stupcem za boju, korišten u labosu
data_pca - dataset stvoren za scatter plot pc1 i pc2 komponenti, dobiven primjenom PCA na data_no_color, korišten u labosu

opis prikaza:
heatmap i scatter plot po uzoru na prošlogodišnji labos, 
prikazuje pjesme izvođača The Weeknd i neke njihove značajke kao što su tempo, energičnost, akustičnost, trajanje itd. i pripadni scatter plot proveden nad istim.
Detaljniji opis pojedinih značajki može se naći na linku originalnog dataseta.

Zrinka Pećanić 0036517187