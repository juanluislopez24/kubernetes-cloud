source activate cloud


cd ads
export FLASK_APP=ads.py
flask run -p 8081 &
cd ..

cd exclusion
export FLASK_APP=exclusion.py
flask run -p 8082 &
cd ..

cd targeting
export FLASK_APP=targeting.py
flask run -p 8083 &
cd ..

cd matching
export FLASK_APP=matching.py
flask run -p 8084 &
cd ..

cd ranking
export FLASK_APP=ranking.py
flask run -p 8085 &
cd ..

cd pricing
export FLASK_APP=pricing.py
flask run -p 8086 &
cd ..
