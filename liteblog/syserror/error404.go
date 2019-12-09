package syserror

type Error404 struct {
	UnKnowError
}

func (this Error404)Code() int{
	return 10002

}
func (this Error404)Error() string{
	if len(this.msg) == 0{
		return "非法路径url"
	}
	return this.msg
}

