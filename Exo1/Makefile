.PHONY: all clean fclean re

all:
	docker-compose up -d --build

clean:
	docker-compose down

fclean:
	docker-compose down --rmi all

re: fclean all
