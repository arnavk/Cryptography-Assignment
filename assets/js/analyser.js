var ciphertext = "";
var map = {};
var frequencyMap = {};
var bigramFrequencyMap = {};
var trigramFrequencyMap = {};
$('#cipher').bind('input propertychange', function() {
	updateCipherText();
});

$(document).ready(function() {
	$("#analyse_button").click(function() {
		analyse();
	});
	var alphabet = "abcdefghijklmnopqrstuvwxyz".split("");
	for (var i in alphabet)
	{
		c = alphabet[i];
		frequencyMap[c] = 0;
	}
});

function updateCipherText()
{
	var s = $('#cipher').val();
	ciphertext = s.toLowerCase();
}

function analyse () {
	updateCipherText();
	var alphabet = "abcdefghijklmnopqrstuvwxyz".split("");
	for (var i in alphabet)
	{
		c = alphabet[i];
		frequencyMap[c] = 0;
	}
	for (var i = 0; i < ciphertext.length; i ++)
	{
		if (frequencyMap[ciphertext[i]] != null)
			frequencyMap[ciphertext[i]]++;
	}
	// console.log (frequencyMap);
	updateFrequencyTable();
}

function updateFrequencyTable ()
{
	$( "#frequencyTable" ).remove();
	var values = [];
	for (var key in frequencyMap)
	{
		values.push(frequencyMap[key]);
	}
	var maxFreqString = Math.max.apply(Math, values) + '';
	var sum = (values.reduce(function(prev, cur) {
		return prev + cur;
	}));

	values = [];
	for (var key in frequencyMap)
	{
		var value = frequencyMap[key] + '';
		while (value.length < maxFreqString.length)
		{
			value = '0' + value;
		}
		values.push(value + '|' + key);
	}
	values.sort();
	values.reverse();

	var html = '<table  class="table table-bordered table-condensed" id="frequencyTable"><thead><tr><td colspan="3">Ciphertext given above</td></tr><tr><td>Letter</td><td>Abs. freq.</td><td>Rel. freq.</td></tr></thead><tbody>';
	for(var i = 0; i < 26; i++)
	{
		var rowValues = values[i].split('|');

		html += '<tr>';
		html += '<td>' + rowValues[1].toUpperCase() + '</td>';
		html += '<td>' + parseInt(rowValues[0]) + '</td>';
		html += '<td>' + ((rowValues[0]*100/sum).toFixed(2)) + '</td>';	
		html += "</tr>";
	}
		
	html += '</tbody></table>';
	$(html).appendTo('#frequencyTableDiv');
	updateBigramFrequencies();

}

function updateBigramFrequencies()
{
	//updateCipherText();
	bigramFrequencyMap = {};
	for (var i = 0; i < ciphertext.length-1; i ++)
	{
		var bigram = ciphertext.substring(i, i+2);
		if ( /^[a-z]+$/i.test ( bigram ) ) {
			if (bigramFrequencyMap[bigram] != null)
				bigramFrequencyMap[bigram] ++;
			else
				bigramFrequencyMap[bigram] = 0;
		}
	}
	console.log(bigramFrequencyMap);
	updateBigramTable();
}

function updateBigramTable()
{
	$( "#bigramTable" ).remove();
	var values = [];
	for (var key in bigramFrequencyMap)
	{
		values.push(bigramFrequencyMap[key]);
	}
	var maxFreqString = Math.max.apply(Math, values) + '';
	// var sum = (values.reduce(function(prev, cur) {
	// 	return prev + cur;
	// }));

	values = [];
	for (var key in bigramFrequencyMap)
	{
		var value = bigramFrequencyMap[key] + '';
		while (value.length < maxFreqString.length)
		{
			value = '0' + value;
		}
		values.push(value + '|' + key);
	}
	values.sort();
	values.reverse();

	var html = '<table  class="table table-bordered table-condensed" id="bigramTable"><thead><tr><td colspan="3">Ciphertext given above</td></tr><tr><td>Letter</td><td>Abs. freq.</td></tr></thead><tbody>';
	for(var i = 0; i < 25; i++)
	{
		var rowValues = values[i].split('|');

		html += '<tr>';
		html += '<td>' + rowValues[1].toUpperCase() + '</td>';
		html += '<td>' + parseInt(rowValues[0]) + '</td>';
		// html += '<td>' + ((rowValues[0]*100/sum).toFixed(2)) + '</td>';	
		html += "</tr>";
	}
		
	html += '</tbody></table>';
	$(html).appendTo('#bigramTableDiv');
	updateTrigramFrequencies();
}

function updateTrigramFrequencies()
{
	updateCipherText();
	trigramFrequencyMap = {};
	for (var i = 0; i < ciphertext.length-1; i ++)
	{
		var trigram = ciphertext.substring(i, i+3);
		if ( /^[a-z]+$/i.test ( trigram ) ) {
			if (trigramFrequencyMap[trigram] != null)
				trigramFrequencyMap[trigram] ++;
			else
				trigramFrequencyMap[trigram] = 0;
		}
	}
	console.log(trigramFrequencyMap);
	updateTrigramTable();
}
function updateTrigramTable()
{
	$( "#trigramTable" ).remove();
	var values = [];
	for (var key in trigramFrequencyMap)
	{
		values.push(trigramFrequencyMap[key]);
	}
	var maxFreqString = Math.max.apply(Math, values) + '';
	// var sum = (values.reduce(function(prev, cur) {
	// 	return prev + cur;
	// }));

	values = [];
	for (var key in trigramFrequencyMap)
	{
		var value = trigramFrequencyMap[key] + '';
		while (value.length < maxFreqString.length)
		{
			value = '0' + value;
		}
		values.push(value + '|' + key);
	}
	values.sort();
	values.reverse();

	var html = '<table  class="table table-bordered table-condensed" id="trigramTable"><thead><tr><td colspan="3">Ciphertext given above</td></tr><tr><td>Letter</td><td>Abs. freq.</td></tr></thead><tbody>';
	for(var i = 0; i < 25; i++)
	{
		var rowValues = values[i].split('|');

		html += '<tr>';
		html += '<td>' + rowValues[1].toUpperCase() + '</td>';
		html += '<td>' + parseInt(rowValues[0]) + '</td>';
		// html += '<td>' + ((rowValues[0]*100/sum).toFixed(2)) + '</td>';	
		html += "</tr>";
	}
		
	html += '</tbody></table>';
	$(html).appendTo('#trigramTableDiv');
}