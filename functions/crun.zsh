crun() {
    local filename="${1%.*}"
    clang "$1" -Wall -o "$filename" && "./$filename" 
}
