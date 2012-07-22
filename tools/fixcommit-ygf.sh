git filter-branch --commit-filter '
        if [ "$GIT_COMMITTER_NAME" = "ygf" ];
        then
                GIT_COMMITTER_NAME="Yasser González Fernández";
                GIT_AUTHOR_NAME="Yasser González Fernández";
                GIT_COMMITTER_EMAIL="ygonzalezfernandez@gmail.com";
                GIT_AUTHOR_EMAIL="ygonzalezfernandez@gmail.com";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD
