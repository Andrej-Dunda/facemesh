const deleteModal = new bootstrap.Modal(document.getElementById('delete-db-log-modal'), {})
let activeLogId = "1";

const openModal = (openedLogId) => {
  console.log("Modal opened")
  activeLogId = openedLogId;
  deleteModal.show();
}

const deleteLog = () => {
  console.log(`Log ${activeLogId} deleted.`);
  deleteModal.hide();
  fetch(`/delete-user-log?delete_log_id=${activeLogId}`, {
    method: 'DELETE'
  })
    .then(response => {
      if (response.ok) {
        location.reload();
      } else {
        console.error('Deletion request failed with status:', response.status);
      }
    })
    .catch(error => {
      console.error('Error occurred during deletion:', error);
    });
}