// Categories
CREATE (men:Category {name: "Men"}),
       (women:Category {name: "Women"}),
       (outer:Category {name: "Outerwear"});

// Designers
CREATE (d1:Designer {name: "Elena Torres"}),
       (d2:Designer {name: "Marco Ruiz"});

// Materials
CREATE (cotton:Material {type: "Cotton"}),
       (linen:Material {type: "Linen"}),
       (leather:Material {type: "Leather"});

// Products
CREATE (p1:Product {name: "Slim Fit Blazer", price: 4999}),
       (p2:Product {name: "High Waist Jeans", price: 2999}),
       (p3:Product {name: "Leather Jacket", price: 7999});

// Product -> Category
CREATE (p1)-[:BELONGS_TO]->(men),
       (p2)-[:BELONGS_TO]->(women),
       (p3)-[:BELONGS_TO]->(outer);

// Product -> Designer
CREATE (p1)-[:DESIGNED_BY]->(d1),
       (p2)-[:DESIGNED_BY]->(d1),
       (p3)-[:DESIGNED_BY]->(d2);

// Product -> Material
CREATE (p1)-[:MADE_OF]->(linen),
       (p2)-[:MADE_OF]->(cotton),
       (p3)-[:MADE_OF]->(leather);
