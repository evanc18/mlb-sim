import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getAnalytics } from "firebase/analytics"


const firebaseConfig = {
    apiKey: "AIzaSyCJ0VdzaXkRk__CDgeVKO9rW9CBseOLAXc",
    authDomain: "gnome-baseball.firebaseapp.com",
    projectId: "gnome-baseball",
    storageBucket: "gnome-baseball.appspot.com",
    messagingSenderId: "275475085803",
    appId: "1:275475085803:web:adc64ad0a5d55e5c6dc1ae",
    measurementId: "G-QXGGFT89N0"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export const auth = getAuth(app);
export const firestore = getFirestore(app);
export default app;
