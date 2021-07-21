# Not working - use ImageMagick's convert program
for fn in data/leaflets/*
do
echo $fn
fn=`python -c "print('$fn'.split('/')[-1])"`
sips -s format pdf "\"$fn\"" --out "\"results/pdfleaflets/${fn%.jpg}.pdf\""
done

