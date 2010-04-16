/* Tiger standard library functions. */

/* Print the string on the standard output. */
void tiger_print(struct tiger_string *s)
{
	if (s->length > 0)
	{
		fwrite(s->data, s->length, 1, stdout);
	}
}

/* Print the integer on the standard output. */
void tiger_printi(int64_t n)
{
	fprintf(stdout, "%lld", n);
}

/* Flush the standard output buffer. */
void tiger_flush()
{
	fflush(stdout);
}

/* Read and return a character from standard input; 
 * return an empty string at end-of-file. */
struct tiger_string *tiger_getchar()
{
	int c;
	struct tiger_string *dest;

	dest = (struct tiger_string *) pytiger2c_malloc(sizeof(struct tiger_string));
	c = fgetc(stdin);
	if (c == EOF)
	{
		dest->data = NULL;
		dest->length = (size_t) 0;
	}
	else
	{
		dest->data = (char *) pytiger2c_malloc(sizeof(char));
		dest->data[0] = (char) (c % 256);
		dest->length = (size_t) 1;
	}

	return dest;
}

/* Return the ASCII value of the first character of s,
 * or -1 if s is empty. */
int64_t tiger_ord(struct tiger_string *s)
{
	if (s->length == 0)
	{
		return (int64_t) -1;
	}
	else
	{
		return (int64_t) s->data[0];
	}
}

/* Return a single-character string for ASCII value i.
 * Terminate program if i is out of range. */
struct tiger_string *tiger_chr(int64_t i)
{
	struct tiger_string *dest;

	if (i < 0 || i > 255)
	{
		pytiger2c_error("chr() function invoked with an invalid ASCII value.");
	}
	dest = (struct tiger_string *) pytiger2c_malloc(sizeof(struct tiger_string));
	dest->data = (char *) pytiger2c_malloc(sizeof(char));
	dest->data[0] = (char) (i % 256);
	dest->length = (size_t) 1;

	return dest;
}

/* Return the number of characters in s. */
int64_t tiger_size(struct tiger_string *s)
{
	return s->length;
}

/* Return the substring of s starting at the character f (first
 * character is numbered zero) and going for n characters. */
struct tiger_string *tiger_substring(struct tiger_string *s, int64_t f, int64_t n)
{
	struct tiger_string *sub;

	if (f < 0 || f + n > s->length)
	{
		pytiger2c_error("substring() invoked with indexes out of range.");
	}
	sub = (struct tiger_string *) pytiger2c_malloc(sizeof(struct tiger_string));
	sub->data = (char *) pytiger2c_malloc(n * sizeof(char));
	sub->length = (size_t) n;
    memcpy(sub->data, s->data + f, n);

    return sub;
}

/* Return a new string consisting of s1 followed by s2. */
struct tiger_string *tiger_concat(struct tiger_string *s1, struct tiger_string *s2)
{
	struct tiger_string *conc;
	size_t conc_len;

	conc_len = s1->length + s2->length;
    conc = (struct tiger_string *) pytiger2c_malloc(sizeof(struct tiger_string));
    conc->data = (char *) pytiger2c_malloc(conc_len * sizeof(char));
    conc->length = conc_len;
    memcpy(conc->data, s1->data, s1->length);
    memcpy(conc->data + s1->length, s2->data, s2->length);

    return conc;
}

/* Return 1 if i is zero, 0 otherwise. */
int64_t tiger_not(int64_t i)
{
	if (i == 0)
	{
		return (int64_t) 1;
	}
	else
	{
		return (int64_t) 0;
	}
}

/* Terminate execution of the program with code i. */
int64_t tiger_exit(int64_t i)
{
	exit((int) i);
}

/* Internal functions used by PyTiger2C. */

/* Print the given runtime error message to stderr and exit
 * the program with error status. */
void pytiger2c_error(char *msg)
{
	fprintf(stderr, "Runtime Error: %s\n", msg);
	exit(EXIT_FAILURE);
}

/* Wrapper malloc to print a runtime error if could not allocate memory. */
void *pytiger2c_malloc(size_t size)
{
	void *mem;

	mem = malloc(size);
	if (mem == NULL)
	{
		pytiger2c_error("Could not allocate memory.");
	}
	memset(mem, 0, size);

	return mem;
}

/* Functions defined in the program. */

