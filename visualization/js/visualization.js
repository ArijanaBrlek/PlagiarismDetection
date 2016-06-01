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

      reader.onload = function(event) {
        var jsonObj = JSON.parse(event.target.result);
        console.log(jsonObj);

          jQuery.get('/data/src/' + jsonObj.src_file, function(data) {
               $('#src-doc').html(data);

                var p = $('#src-doc')[0],
                    textArray = p.innerText.split('');

                jsonObj.fragments.forEach(function (fragment) {
                    textArray[fragment.src_offset] = '<span style="background-color:yellow">' + textArray[fragment.src_offset];
                    textArray[fragment.src_len + fragment.src_offset] = '</span>' + textArray[fragment.src_len + fragment.src_offset];
                });

                $('#src-doc')[0].innerHTML = textArray.join('');
            });

          jQuery.get('/data/susp/' + jsonObj.susp_file, function(data) {
               $('#susp-doc').html(data);

                var p = $('#susp-doc')[0],
                    textArray = p.innerText.split('');

                jsonObj.fragments.forEach(function (fragment) {
                    textArray[fragment.susp_offset] = '<span style="background-color:yellow">' + textArray[fragment.susp_offset];
                    textArray[fragment.susp_len + fragment.susp_offset] = '</span>' + textArray[fragment.susp_len + fragment.susp_offset];
                });

                $('#susp-doc')[0].innerHTML = textArray.join('');
            });


      };

      reader.readAsText(event.target.files[0]);
    });
});