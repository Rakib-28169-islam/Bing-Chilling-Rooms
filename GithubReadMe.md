# Bing-Chilling-Rooms Git Setup

## Step-by-step Git Commands:

# If You Don't Create the project folder on Your Local Pc Then Follow from step 1,2
# 1. Initialize local repo (if not already)

git init

# 2. Add the remote repository
git remote add origin https://github.com/Rakib-28169-islam/Bing-Chilling-Rooms.git

# 3. Fetch all branches from the remote
git fetch origin

# 4. Checkout  friend's branch (example: Rakib)
git checkout -b Rakib origin/Rakib
# this command will download all files from Rakib Branch

# 5. Create your own branch
git checkout -b your_name
# *** Must Create Your Repo Then push your code Unless it will mixed up with another Branches code

# 6. Push your own branch to GitHub
git push origin Hasib

# 7. Make your changes and stage them
git add .

# 8. Commit your changes
git commit -m "Your commit message"

# 9. Push changes to your own branch
git push origin Hasib
