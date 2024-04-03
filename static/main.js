function confirmDelete(postId) {
    if (confirm("Are you sure you want to delete this post?")) {
        const deleteUrl = `/delete/${postId}`;
        fetch(deleteUrl, {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                // If deletion is successful, remove the post element from the DOM
                const postElement = document.getElementById(`post_${postId}`);
                postElement.remove();
            } else {
                console.error('Failed to delete the post');
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    }
}


function likePost(postId) {
        // Send an AJAX request to the Flask route for liking a post
        fetch('/like/' + postId, {
            method: 'POST'
        }).then(response => {
            if (response.ok) {
                // Update the number of likes displayed on the page
                const likesElement = document.getElementById('likes_' + postId);
                likesElement.textContent = parseInt(likesElement.textContent) + 1;
            } else {
                console.error('Failed to like the post');
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    }
