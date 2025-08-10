# Authentication (Firebase)

## One-time Setup
1. Go to **Firebase Console** → **Build → Authentication → Sign-in method**.
2. Enable **Email/Password** (you can also enable **Google** sign-in if desired).
3. Go to **Settings → Authorized domains** and ensure `localhost` and `127.0.0.1` are listed.  
   When deploying to a web server, update this to include your production domain.

---

## Create a Test User
1. In the **Firebase Console**, navigate to **Authentication → Users → Add user**.
2. Enter an **email** and **password** (you’ll use these to sign in from the app).

---

## Local Environment (Vite)
There is a `.env` file inside `demo-cand/` containing Firebase configuration variables.  
These can be updated to match your Firebase project:

```env
VITE_FIREBASE_API_KEY=YOUR_KEY
VITE_FIREBASE_AUTH_DOMAIN=webofinfluence-a55f9.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=webofinfluence-a55f9
VITE_FIREBASE_APP_ID=YOUR_APP_ID
```

After editing, restart the dev server.

## Run the app
``` 
cd demo-cand
npm install
npm run dev
```

open http://localhost:5173/WebOfInfluenceResearch/login


## App behavior
- All routes except `/login` are protected.
- Use the test user you created in **Authentication → Users** to sign in.
- Use **Settings** page to view your email and send a password reset email.
- Use **Logout** to fully sign out (Firebase `signOut`), then you’ll be redirected to `/login`.

## Troubleshooting
- **auth/configuration-not-found** → enable the provider(s) in **Sign‑in method**.
- **auth/invalid-credential** → wrong email/password or no user exists (create one in **Users**).
- If you later expose the site via a tunnel (e.g., ngrok), add that domain to **Authorized domains**.

