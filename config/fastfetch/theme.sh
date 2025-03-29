
time3="8/26/2024 9:00PM"
let current=$(date +%s)
timestamp3=$(date -d "$time3" +%s)
theme_progression=$((current - timestamp3))
theme_done=$((theme_progression/ 86400))


echo $theme_done Days on Solarized
