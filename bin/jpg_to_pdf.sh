for fn in leaflets/*
do
echo $fn
sips -s format pdf "$fn" --out "pdfleaflets/${fn%.jpg}.pdf"
done

