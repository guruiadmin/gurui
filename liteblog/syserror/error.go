package syserror

type Error interface {
	Code() int
	Error() string
	ReasonError() error
}

func New(msg string, reaso error) Error{
	return UnKnowError{msg,reaso}
}