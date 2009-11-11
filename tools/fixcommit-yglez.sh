git filter-branch --commit-filter '
        if [ "$GIT_COMMITTER_NAME" = "yasserglez" ];
        then
                GIT_COMMITTER_NAME="Yasser González Fernández";
                GIT_AUTHOR_NAME="Yasser González Fernández";
                GIT_COMMITTER_EMAIL="yglez@uh.cu";
                GIT_AUTHOR_EMAIL="yglez@uh.cu";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD
