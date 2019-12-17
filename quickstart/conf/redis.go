package conf

import (
	"github.com/astaxie/beego"
	"github.com/gomodule/redigo/redis"
	"time"
)

var (
	RedisClient *redis.Pool
	Radishes    string
	Reimport    string
	Redid       int
)

func init() {
	//设置redis连接ip
	Radishes = beego.AppConfig.String("redis.host")
	//设置redis端口
	Reimport = beego.AppConfig.String("redis.port")
	//设置redis数据库名
	Redid, _ = beego.AppConfig.Int("redis.db")
	//建立连接池
	RedisClient = &redis.Pool{
		//设置redis最大空闲数
		MaxIdle: beego.AppConfig.DefaultInt("redis.max.idle", 1),
		//设置redis最大连接数
		MaxActive: beego.AppConfig.DefaultInt("redis.max.active", 10),
		//设置连接超时时间
		IdleTimeout: 180 * time.Second,
		Dial: func() (redis.Conn, error) {
			c, err := redis.Dial("tcp", Radishes+":"+Reimport)
			if err != nil {
				return nil, err
			}
			//连接数据库
			c.Do("SELECT", Redid)
			return c, nil
		},
	}
}
