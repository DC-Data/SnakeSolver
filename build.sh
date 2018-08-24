pyenv install -s 3.7.0
virtualenv -p ~/.pyenv/versions/3.7.0/bin/python --clear --always-copy --no-site-packages venv

source venv/bin/activate
pip3 install -r requirements.txt
deactivate

curl -o pre-commit.sh https://raw.githubusercontent.com/google/yapf/master/plugins/pre-commit.sh
chmod a+x pre-commit.sh
sed -i '' '2s/^/export PATH=\/usr\/local\/bin:$PATH/' pre-commit.sh  # for sourcetree
mv pre-commit.sh .git/hooks/pre-commit
