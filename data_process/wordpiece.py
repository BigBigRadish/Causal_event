# -*- coding: utf-8 -*-
'''
Created on 2019年2月27日

@author: Zhukun Luo
Jiangxi university of finance and economics
'''
class WordpieceTokenizer(object):

    """Runs WordPiece tokenziation."""
    def __init__(self, vocab, unk_token="[UNK]", max_input_chars_per_word=100):
        self.vocab = vocab    
        self.unk_token = unk_token    
        self.max_input_chars_per_word = max_input_chars_per_word

    def tokenize(self, text):
        """Tokenizes a piece of text into its word pieces.
        This uses a greedy longest-match-first algorithm to perform tokenization
        using the given vocabulary. 
        For example:
        input = "unaffable" 
        output = ["un", "##aff", "##able"] 
        Args:  
        text: A single token or whitespace separated tokens.
        This should have already been passed through `BasicTokenizer. 
        Returns: A list of wordpiece tokens.
        """    
        text = convert_to_unicode(text)
        output_tokens = []
        for token in whitespace_tokenize(text):
            chars = list(token) 
            if len(chars) > self.max_input_chars_per_word: 
                output_tokens.append(self.unk_token)
                continue
            
            is_bad = False
            start = 0
            sub_tokens = []
            while start < len(chars):
                end = len(chars)
                cur_substr = None
                while start < end:
                    substr = "".join(chars[start:end])
                    if start > 0:
                        substr = "##" + substr
                    if substr in self.vocab:
                        cur_substr = substr
                        break
                    end -= 1
                if cur_substr is None:
                    is_bad = True
                    break
                sub_tokens.append(cur_substr)
                start = end
            if is_bad:
                output_tokens.append(self.unk_token)
            else:
                output_tokens.extend(sub_tokens)
        return output_tokens
