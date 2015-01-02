module Mission

	@adjectives = []
	@nouns = []
	@colors = []
	@animals = []
	@mission_grammars = []


	def Mission.get_name()
		adj, bad_nouns = get_adj();
		noun = get_noun(bad_nouns)

		adj2 = adj
		noun2 = noun
		while adj2[0] == adj[0] || noun2 == noun
			adj2, bad_nouns = get_adj();
			noun2 = get_noun(bad_nouns)
		end

		color = get_color()
		animal = get_animal()

		name = ""
		case rand(1..100)
		when 1..10
			name += "Project "
		when 11..20
			name += "Operation "
		end

		total_prob = 0
		@mission_grammars.each{|grammar| 
			grammar[0] = grammar[0].to_i
			total_prob += grammar[0]
		}
		chance = rand(1..total_prob)
		@mission_grammars.each{|grammar|
			if chance < grammar[0]
				name += eval(grammar[1])
				break
			end
			chance -= grammar[0]
		}

		return name
	end
end
