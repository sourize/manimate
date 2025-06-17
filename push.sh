#!/bin/bash

# Push to Hugging Face
echo "Pushing to Hugging Face..."
git push origin main

# Push to GitHub
echo "Pushing to GitHub..."
git push github main

echo "Done!" 