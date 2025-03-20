# WAD2_BinThere_Project
## Group 6D's WAD2 WebApp Design Project

### What is it?​

♻️ The application is designed to help users find recycling bins around and close to the campus and find out what types of waste they can dispose of at each bin location.​

♻️ The application uses an interactive map where users can search for bin locations and bin types (e.g., PET bottle, glass, soft plastic).​

♻️ Registered users can add new locations, update bin types, and verify if bins still exist by upvoting or downvoting to ensure that the information remains up to date.​

📌 **Core Purpose**​

♻️ To encourage recycling by making it easier for people to find the right recycling bin.​

---

## Original Specification ​

✔️ **User Authentication** ​

📇 Users can create an account and change their password​.

🗺️ **Map API** – Leaflet.js is used for an interactive map where users can add bin locations​.

➕ Logged-in users can add bin types to bin locations​.

➖ Admins can delete and edit locations and bin types​.

👍 Logged-in users can upvote or downvote bins based on their existence.

---

## **Revised Specification**

✔️ **Bin List Page** - A dedicated page listing all bins with improved accessibility.

➕ **Logged-in users can now create new bins.**

🗑️ **Users can delete their own bins.**

✏️ **Users can edit bin types but cannot edit bin locations.**

👤 **Users can view which user added a bin.**

🖼️ **Users can optionally add a profile picture and/or a description for the bin.**

🔍 **Users can search for bins**:
   - By location name.
   - By bin type.
   - Using geopy to search via location.

🔄 **Users can reset their search in the bin list to review all bins without refreshing the page.**

👥 **Users can view a list of all registered users.**

🌐 **Users can add a website link to their profile.**

🖼️ **Users can upload a profile picture. If none is provided, a default image is used.**

✨ **Default Profile Picture added to all entries to enhance readability and presentation.**

❓ **Users can access a user guide.**

---

## **References and Additional Packages**

### Websites
- **Favicon Generator** - [Favicon.io](https://favicon.io/favicon-converter/)

### **Images**
- **Favicon** - [Green Bin with Leaf Logo](https://c8.alamy.com/comp/2HKEJ26/rubbish-bin-green-with-leaf-logo-design-vector-graphic-symbol-icon-illustration-creative-idea-2HKEJ26.jpg)
- **Green Leaf Picture** - [Freepik](https://img.freepik.com/premium-vector/eco-circle-with-hand-logo_78370-3923.jpg?w=2000)
- **Rubbish in Bin** - [VectorStock](https://cdn1.vectorstock.com/i/1000x1000/55/65/put-rubbish-in-the-bin-vector-23855565.jpg)
- **Default Profile Picture 1** - [Dj Cat Image](https://archive.org/details/cat-meme-stock/素材/DJ猫.mp4)
- **Default Profile Picture 2** - [Bing Image Search](https://www.bing.com/images/search?view=detailV2&ccid=5GpH%2FATc&id=3CD6A2508F665A758A9E00ED778DF7BC0013B9F8&thid=OIP.5GpH_ATcZ3MIdbnMNJNG8AHaHa&mediaurl=https%3A%2F%2Fstatic.vecteezy.com%2Fsystem%2Fresources%2Fpreviews%2F010%2F852%2F913%2Foriginal%2Fleaf-icon-vector-png.png)
- **Default Profile Picture 3** - [Technology LinkedIn Background](https://wallpapers.com/images/hd/technology-linkedin-background-sj2amwxyouxivqod.jpg)
- **Default Profile Picture 4** - [Bin with Googly Eyes](https://i.pinimg.com/originals/b5/45/95/b54595929d40a4d90f717661bc905ec0.jpg)
- **Default Profile Picture 5** - [Tree Image](https://www.treesaw.co.uk/wp-content/uploads/2020/03/tree-3822149_1920.jpg)
- **Green Bin Icon** - [Freepik](https://www.freepik.com/icon/can_14863152#fromView=keyword&page=1&position=94&uuid=27a10ac2-d9fa-42d7-9951-86fcb72141ad)
- **Created Account Default Profile Picture** - [Vecteezy](https://static.vecteezy.com/system/resources/thumbnails/037/336/395/small_2x/user-profile-flat-illustration-avatar-person-icon-gender-neutral-silhouette-profile-picture-free-vector.jpg)

### **External Packages**
- **Leaflet JavaScript Package** - [Leaflet.js](https://leafletjs.com/index.html)
  - JavaScript: [Leaflet.js](https://unpkg.com/leaflet/dist/leaflet.js)
  - CSS: [Leaflet.css](https://unpkg.com/leaflet/dist/leaflet.css)
- **Coverage** - Installed via `pip install` - [Coverage Docs](https://coverage.readthedocs.io/en/7.7.0/)
- **Geopy** - Installed via `pip install` - [Geopy Docs](https://geopy.readthedocs.io/en/stable/)



