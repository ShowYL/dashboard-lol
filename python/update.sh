
echo -e "1) Run the full update
2) Run the update.py and the patch.py
3) Run the patch.py and upload_pantry.py
4) Run the update.py
5) Run the patch.py
6) Run the upload_pantry.py"

read -p "Number : " answer

case $answer in
    1)
        output=$(python -u ./update.py | tee /dev/tty)

        if [[ "$output" != *"Patch up to date"* ]]; then
            python ./patch.py
            python ./upload_pantry.py
        fi

        echo -e "\e[32mEverything up to Date\e[0m"
        ;;
    2)
        python -u ./update.py
        python ./patch.py
        ;;
    3)
        python ./patch.py
        python ./upload_pantry.py
        ;;
    4)
        python -u ./update.py
        ;;
    5)
        python ./patch.py
        ;;
    6)
        python ./upload_pantry.py
        ;;
    *)
        echo "You've choose nothing valid"
        ;;
esac