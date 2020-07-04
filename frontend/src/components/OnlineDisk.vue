    downloadFile(fileId) {
      try {
        console.log(fileId)
        var elemIF = document.createElement('iframe')
        elemIF.src = '/download?file_id=' + fileId
        elemIF.style.display = 'none'
        document.body.appendChild(elemIF)
      } catch (e) {
        console.log(e);
        this.$message({
          message: e.response.data.msg,
          type: "error"
        });
      }
    },
