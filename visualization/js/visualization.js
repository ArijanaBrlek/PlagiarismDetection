// var p = document.findElementById('src-doc'),/*
//     textArray = p.innerText.split(''),
//     highlights = [{ start: 0, length: 5 }, { start: 22, length: 10 }];
//
// highlights.forEach(function (highlight) {
//     textArray[highlight.start] = '<span style="background-color:yellow">' + textArray[highlight.start];t
//     textArray[highlight.length + highlight.start] = '</span>' + textArray[highlight.length + highlight.start];
// });
// */
// p.innerHTML = textArray.join('');

$(function() {

    $(document).on('change', '.file-upload-button', function(event) {
      var reader = new FileReader();

      $('#filename').val(event.target.files[0].name);

      reader.onload = function(event) {

        var jsonObj = JSON.parse(event.target.result);

        $('#src-filename').html(jsonObj.src_file);
        $('#susp-filename').html(jsonObj.susp_file);

          jQuery.get('/data/test_corpus/src/' + jsonObj.src_file, function(data) {
               $('#src-doc').html(data);

                var p = $('#src-doc')[0],
                    textArray = data.split('');

                jsonObj.fragments.forEach(function (fragment) {
                    fragment.src_offset = parseInt(fragment.src_offset, 10);
                    fragment.src_len = parseInt(fragment.src_len, 10);

                    textArray[fragment.src_offset] = '<span style="background-color:yellow">' + textArray[fragment.src_offset];
                    textArray[fragment.src_len + fragment.src_offset] = '</span>' + textArray[fragment.src_len + fragment.src_offset];
                });

                $('#src-doc')[0].innerHTML = textArray.join('');
            });

          jQuery.get('/data/test_corpus/susp/' + jsonObj.susp_file, function(data) {
               $('#susp-doc').html(data);

                var p = $('#susp-doc')[0],
                    textArray = data.split('');

                jsonObj.fragments.forEach(function (fragment) {
                    fragment.susp_offset = parseInt(fragment.susp_offset, 10);
                    fragment.susp_len = parseInt(fragment.susp_len, 10);

                    textArray[fragment.susp_offset] = '<span style="background-color:yellow">' + textArray[fragment.susp_offset];
                    textArray[fragment.susp_len + fragment.susp_offset] = '</span>' + textArray[fragment.susp_len + fragment.susp_offset];
                });

                $('#susp-doc')[0].innerHTML = textArray.join('');
            });


      };

      reader.readAsText(event.target.files[0]);
    });
});